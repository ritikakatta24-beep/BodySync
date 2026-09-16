from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)

# Load trained model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model",
    "workout_type_recommendation_model.joblib"
)

model = joblib.load(MODEL_PATH)

# Fields expected from the user (BMI removed)
EXPECTED_COLUMNS = [
    "age",
    "gender",
    "height_cm",
    "weight_kg",
    "target_weight",
    "goal",
    "fitness_level",
    "intensity_preference",
    "primary_focus",
    "equipment_access"
]

# Allowed values for categorical features
ALLOWED_VALUES = {
    "gender": ["male", "female"],
    "goal": [
        "general_fitness",
        "endurance",
        "muscle_gain",
        "weight_loss",
        "flexibility"
    ],
    "fitness_level": [
        "beginner",
        "intermediate",
        "advanced"
    ],
    "intensity_preference": [
        "low",
        "moderate",
        "high"
    ],
    "primary_focus": [
        "core_strength",
        "mind_body_relaxation",
        "muscle_building",
        "strength_toning",
        "cardio_endurance",
        "stamina_building",
        "fat_burning",
        "calorie_burn_intensity",
        "overall_toning",
        "general_wellness"
    ],
    "equipment_access": [
        "bodyweight_only",
        "dumbbells_home",
        "kettlebell_home",
        "resistance_bands",
        "full_gym",
        "cardio_machine",
        "yoga_mat"
    ]
}


def validate_input(data):
    """Returns an error message if invalid, else None."""

    # Check missing fields
    missing = [col for col in EXPECTED_COLUMNS if col not in data]
    if missing:
        return f"Missing required fields: {missing}"

    # Validate categorical fields
    for col, allowed in ALLOWED_VALUES.items():
        if data[col] not in allowed:
            return f"Invalid value for '{col}'. Expected one of {allowed}"

    # Validate numeric fields
    numeric_cols = [
        "age",
        "height_cm",
        "weight_kg",
        "target_weight"
    ]

    for col in numeric_cols:
        try:
            float(data[col])
        except (ValueError, TypeError):
            return f"'{col}' must be a number."

    return None


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    error = validate_input(data)

    if error:
        return jsonify({"error": error}), 400

    try:

        # Calculate BMI automatically
        height_cm = float(data["height_cm"])
        weight_kg = float(data["weight_kg"])

        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)

        # Create dataframe exactly as the model expects
        input_df = pd.DataFrame([{
            "age": data["age"],
            "gender": data["gender"],
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "target_weight": data["target_weight"],
            "bmi": bmi,
            "goal": data["goal"],
            "fitness_level": data["fitness_level"],
            "intensity_preference": data["intensity_preference"],
            "primary_focus": data["primary_focus"],
            "equipment_access": data["equipment_access"]
        }])

        prediction = model.predict(input_df)[0]

        response = {
            "workout_type": prediction,
            "bmi": round(bmi, 1)
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
