from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model",
    "macro_nutrients_model.joblib"
)
model = joblib.load(MODEL_PATH)

# --- Feature / target definitions (kept here since model is just the
#     raw pipeline now, not a metadata dict) ---
NUMERIC_COLS = ["age", "height_cm", "weight_kg", "target_weight", "bmi"]
CATEGORICAL_COLS = [
    "gender", "goal", "fitness_level", "intensity_preference",
    "primary_focus", "equipment_access", "workout_type",
]
FEATURE_COLS = NUMERIC_COLS + CATEGORICAL_COLS
TARGET_COLS = ["total_calories", "protein_g", "carbs_g", "fats_g"]

ALLOWED_VALUES = {
    "gender": {"male", "female"},
    "goal": {"general_fitness", "endurance", "flexibility", "weight_loss", "muscle_gain"},
    "fitness_level": {"beginner", "intermediate", "advanced"},
    "intensity_preference": {"low", "moderate", "high"},
    "primary_focus": {
        "general_wellness", "stamina_building", "core_strength",
        "calorie_burn_intensity", "fat_burning", "mind_body_relaxation",
        "overall_toning", "cardio_endurance", "muscle_building",
        "strength_toning",
    },
    "equipment_access": {
        "bodyweight_only", "cardio_machine", "yoga_mat",
        "dumbbells_home", "resistance_bands", "full_gym", "kettlebell_home",
    },
    "workout_type": {"HIIT", "cardio", "strength", "yoga", "pilates"},
}

NUMERIC_RANGES = {
    "age": (10, 90),
    "height_cm": (120, 230),
    "weight_kg": (25, 250),
    "target_weight": (25, 250),
    "bmi": (10, 60),
}


def validate_input(data: dict):
    missing = [f for f in FEATURE_COLS if f not in data]
    if missing:
        return False, f"Missing required fields: {missing}"

    for field in NUMERIC_COLS:
        value = data[field]
        if not isinstance(value, (int, float)):
            return False, f"'{field}' must be a number"
        low, high = NUMERIC_RANGES[field]
        if not (low <= value <= high):
            return False, f"'{field}' out of realistic range ({low}-{high})"

    for field in CATEGORICAL_COLS:
        value = data[field]
        if value not in ALLOWED_VALUES[field]:
            return False, (
                f"'{field}' value '{value}' invalid. "
                f"Allowed: {sorted(ALLOWED_VALUES[field])}"
            )

    return True, None


@app.route("/predict", methods=["POST"])
def predict_nutrition():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    is_valid, error = validate_input(data)
    if not is_valid:
        return jsonify({"error": error}), 400

    row = {col: data[col] for col in FEATURE_COLS}
    X = pd.DataFrame([row])

    prediction = model.predict(X)[0]

    result = {
        target: round(float(value), 1)
        for target, value in zip(TARGET_COLS, prediction)
    }
    result["total_calories"] = int(round(result["total_calories"]))

    return jsonify({
        "predicted_nutrition": result,
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)
