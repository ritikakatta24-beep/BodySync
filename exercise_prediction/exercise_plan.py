import os
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load database on startup
DB_PATH = os.path.join(os.path.dirname(__file__), 'exercise_database.csv')
if os.path.exists(DB_PATH):
    df = pd.read_csv(DB_PATH)
else:
    # Creating an empty DataFrame as fallback if file is missing
    df = pd.DataFrame()

VALID_WORKOUT_TYPES = ['yoga', 'cardio', 'hiit', 'strength', 'pilates']
VALID_FITNESS_LEVELS = ['beginner', 'intermediate', 'advanced']
VALID_GENDERS = ['male', 'female']
VALID_EQUIPMENT = ['bodyweight_only', 'dumbbells_home', 'kettlebell_home', 'resistance_bands', 'full_gym', 'cardio_machine', 'yoga_mat']

DAY_FOCUS = {
    'strength': [
        {"day": "Monday", "focus": "Chest & Triceps", "groups": ["chest", "arms"]},
        {"day": "Tuesday", "focus": "Back & Biceps", "groups": ["back", "arms"]},
        {"day": "Wednesday", "focus": "Legs & Glutes", "groups": ["legs", "glutes"]},
        {"day": "Thursday", "focus": "Shoulders & Core", "groups": ["shoulders", "core"]},
        {"day": "Friday", "focus": "Arms & Abs", "groups": ["arms", "core"]},
        {"day": "Saturday", "focus": "Full Body", "groups": ["full_body", "mix"]},
        {"day": "Sunday", "focus": "Active Recovery", "groups": ["core", "full_body"]}
    ],
    'cardio': [
        {"day": "Monday", "focus": "Endurance", "groups": ["full_body", "legs"]},
        {"day": "Tuesday", "focus": "Speed & Agility", "groups": ["legs", "full_body"]},
        {"day": "Wednesday", "focus": "Fat Burn", "groups": ["full_body", "core"]},
        {"day": "Thursday", "focus": "Cardio Mix", "groups": ["mix", "full_body", "legs", "core", "arms"]},
        {"day": "Friday", "focus": "Interval Training", "groups": ["full_body", "legs"]},
        {"day": "Saturday", "focus": "Endurance Plus", "groups": ["full_body"]},
        {"day": "Sunday", "focus": "Low Impact Recovery", "groups": ["full_body", "core"]}
    ],
    'hiit': [
        {"day": "Monday", "focus": "Upper Body Blast", "groups": ["chest", "back", "shoulders", "arms"]},
        {"day": "Tuesday", "focus": "Lower Body Blast", "groups": ["legs", "glutes"]},
        {"day": "Wednesday", "focus": "Core & Abs", "groups": ["core"]},
        {"day": "Thursday", "focus": "Full Body Burn", "groups": ["full_body"]},
        {"day": "Friday", "focus": "Tabata Style", "groups": ["mix", "full_body", "legs", "core", "arms", "chest"]},
        {"day": "Saturday", "focus": "Cardio HIIT", "groups": ["full_body", "legs"]},
        {"day": "Sunday", "focus": "Active Recovery", "groups": ["core", "full_body"]}
    ],
    'yoga': [
        {"day": "Monday", "focus": "Sun Salutation Flow", "groups": ["full_body"]},
        {"day": "Tuesday", "focus": "Balance & Flexibility", "groups": ["legs", "core"]},
        {"day": "Wednesday", "focus": "Strength & Stability", "groups": ["arms", "core", "legs"]},
        {"day": "Thursday", "focus": "Deep Stretch", "groups": ["legs", "back", "full_body"]},
        {"day": "Friday", "focus": "Power Flow", "groups": ["full_body"]},
        {"day": "Saturday", "focus": "Restorative", "groups": ["full_body", "back"]},
        {"day": "Sunday", "focus": "Meditation & Yin", "groups": ["full_body", "core"]}
    ],
    'pilates': [
        {"day": "Monday", "focus": "Core Foundation", "groups": ["core"]},
        {"day": "Tuesday", "focus": "Lower Body", "groups": ["legs", "glutes"]},
        {"day": "Wednesday", "focus": "Upper Body", "groups": ["arms", "shoulders", "chest"]},
        {"day": "Thursday", "focus": "Flexibility", "groups": ["full_body", "back"]},
        {"day": "Friday", "focus": "Full Body", "groups": ["full_body"]},
        {"day": "Saturday", "focus": "Core & Glutes", "groups": ["core", "glutes"]},
        {"day": "Sunday", "focus": "Stretch & Release", "groups": ["full_body"]}
    ]
}

@app.route('/api/exercise-plan', methods=['POST'])
def generate_exercise_plan():
    if df.empty:
        return jsonify({"error": "Exercise database not found or empty."}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    workout_type = data.get('workout_type')
    fitness_level = data.get('fitness_level')
    gender = data.get('gender')
    equipment_access = data.get('equipment_access')
    week_number = data.get('week_number', 1)

    # Validate required fields
    if not all([workout_type, fitness_level, gender, equipment_access]):
        return jsonify({"error": "Missing required fields: workout_type, fitness_level, gender, equipment_access"}), 400

    if workout_type not in VALID_WORKOUT_TYPES:
        return jsonify({"error": f"Invalid workout_type. Must be one of {VALID_WORKOUT_TYPES}"}), 400
    if fitness_level not in VALID_FITNESS_LEVELS:
        return jsonify({"error": f"Invalid fitness_level. Must be one of {VALID_FITNESS_LEVELS}"}), 400
    if gender not in VALID_GENDERS:
        return jsonify({"error": f"Invalid gender. Must be one of {VALID_GENDERS}"}), 400
    if equipment_access not in VALID_EQUIPMENT:
        return jsonify({"error": f"Invalid equipment_access. Must be one of {VALID_EQUIPMENT}"}), 400

    try:
        week_number = int(week_number)
    except ValueError:
        return jsonify({"error": "week_number must be an integer."}), 400

    # Filter exercises by workout_type
    filtered = df[df['workout_type'] == workout_type]
    
    # Filter by equipment_access (always include bodyweight_only)
    filtered = filtered[filtered['equipment_needed'].isin([equipment_access, 'bodyweight_only'])]

    if filtered.empty:
        return jsonify({"error": "No exercises found for the given criteria."}), 404

    # Deterministic sorting for rotation
    filtered = filtered.sort_values(by='exercise_name').reset_index(drop=True)

    total_exercises = len(filtered)
    offset = ((week_number - 1) * 28) % total_exercises

    plan_response = {
        "workout_type": workout_type,
        "week_number": week_number,
        "fitness_level": fitness_level,
        "plan": {}
    }

    focus_schedule = DAY_FOCUS[workout_type]

    for i, day_info in enumerate(focus_schedule):
        day_index = i + 1
        day_key = f"day_{day_index}"
        
        target_groups = day_info['groups']
        
        # Filter for this day's muscle groups
        day_exercises = filtered[filtered['muscle_group'].isin(target_groups)].reset_index(drop=True)
        
        # If not enough, fallback to full_body or just any available
        if len(day_exercises) < 4:
            fallback = filtered[filtered['muscle_group'] == 'full_body']
            day_exercises = pd.concat([day_exercises, fallback]).drop_duplicates(subset=['exercise_name']).reset_index(drop=True)
        
        if len(day_exercises) < 4:
            # Still not enough, just take from general filtered
            day_exercises = pd.concat([day_exercises, filtered]).drop_duplicates(subset=['exercise_name']).reset_index(drop=True)

        # Select 5 exercises using offset
        num_to_pick = min(5, len(day_exercises))
        selected = []
        
        for j in range(num_to_pick):
            idx = (offset + j) % len(day_exercises)
            selected.append(day_exercises.iloc[idx])
            
        offset = (offset + num_to_pick) % total_exercises
        
        exercises_list = []
        for ex in selected:
            sets_col = f"sets_{fitness_level}"
            reps_col = f"reps_{fitness_level}"
            weight_col = f"weight_{gender}_{fitness_level}_kg"
            
            ex_data = {
                "name": str(ex['exercise_name']),
                "equipment": str(ex['equipment_needed'])
            }
            
            # Handle sets
            if sets_col in ex and pd.notna(ex[sets_col]):
                ex_data["sets"] = int(ex[sets_col])
                
            # Rest seconds
            if 'rest_seconds' in ex and pd.notna(ex['rest_seconds']):
                ex_data["rest_seconds"] = int(ex['rest_seconds'])

            is_timed = False
            if 'is_timed' in ex:
                is_timed = str(ex['is_timed']).lower() in ['true', '1', 't', 'y', 'yes']

            if workout_type in ['yoga', 'pilates'] or is_timed:
                if reps_col in ex and pd.notna(ex[reps_col]):
                    ex_data["duration_seconds"] = int(ex[reps_col])
            else:
                if reps_col in ex and pd.notna(ex[reps_col]):
                    ex_data["reps"] = int(ex[reps_col])
                    
            if workout_type == 'strength' and weight_col in ex and pd.notna(ex[weight_col]):
                try:
                    weight = float(ex[weight_col])
                    if weight > 0:
                        ex_data["weight_kg"] = weight
                except ValueError:
                    pass

            exercises_list.append(ex_data)

        plan_response["plan"][day_key] = {
            "day": day_info["day"],
            "focus": day_info["focus"],
            "exercises": exercises_list
        }

    return jsonify(plan_response)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
