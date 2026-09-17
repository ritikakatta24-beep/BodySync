import pandas as pd
import os

exercises = []

def add_ex(name, w_type, m_group, diff, s_b, s_i, s_a, r_b, r_i, r_a, rest, wm_b, wm_i, wm_a, wf_b, wf_i, wf_a, eq, timed):
    exercises.append({
        "exercise_name": name,
        "workout_type": w_type,
        "muscle_group": m_group,
        "difficulty": diff,
        "sets_beginner": s_b, "sets_intermediate": s_i, "sets_advanced": s_a,
        "reps_beginner": r_b, "reps_intermediate": r_i, "reps_advanced": r_a,
        "rest_seconds": rest,
        "weight_male_beginner_kg": float(wm_b), "weight_male_intermediate_kg": float(wm_i), "weight_male_advanced_kg": float(wm_a),
        "weight_female_beginner_kg": float(wf_b), "weight_female_intermediate_kg": float(wf_i), "weight_female_advanced_kg": float(wf_a),
        "equipment_needed": eq,
        "is_timed": timed
    })

# 1. Strength (40+)
strength_exercises = [
    ("Barbell Bench Press", "chest", "all", 3, 4, 5, 8, 10, 12, 90, 20, 40, 70, 12, 24, 42, "full_gym"),
    ("Dumbbell Bench Press", "chest", "all", 3, 4, 5, 8, 10, 12, 90, 10, 20, 35, 6, 12, 21, "full_gym"),
    ("Incline Barbell Bench Press", "chest", "all", 3, 4, 4, 8, 8, 10, 90, 20, 35, 60, 12, 21, 36, "full_gym"),
    ("Incline Dumbbell Press", "chest", "all", 3, 4, 4, 8, 10, 12, 90, 10, 18, 30, 6, 10, 18, "full_gym"),
    ("Decline Barbell Bench Press", "chest", "intermediate", 0, 3, 4, 0, 8, 10, 90, 0, 40, 70, 0, 24, 42, "full_gym"),
    ("Push-ups", "chest", "all", 3, 4, 5, 10, 20, 30, 60, 0, 0, 0, 0, 0, 0, "bodyweight_only"),
    ("Cable Crossovers", "chest", "intermediate", 0, 3, 4, 0, 12, 15, 60, 0, 15, 25, 0, 9, 15, "full_gym"),
    ("Dumbbell Flyes", "chest", "all", 3, 3, 4, 10, 12, 15, 60, 5, 10, 18, 3, 6, 10, "dumbbells_home"),
    ("Pec Deck Machine", "chest", "all", 3, 3, 4, 10, 12, 15, 60, 20, 40, 60, 12, 24, 36, "full_gym"),
    ("Resistance Band Chest Press", "chest", "beginner", 3, 4, 0, 12, 15, 0, 60, 0, 0, 0, 0, 0, 0, "resistance_bands"),
    ("Barbell Deadlift", "back", "all", 3, 4, 5, 5, 5, 5, 120, 40, 80, 140, 24, 48, 84, "full_gym"),
    ("Pull-ups", "back", "intermediate", 0, 3, 4, 0, 5, 12, 90, 0, 0, 0, 0, 0, 0, "bodyweight_only"),
    ("Lat Pulldown", "back", "all", 3, 4, 4, 10, 10, 12, 90, 20, 40, 60, 12, 24, 36, "full_gym"),
    ("Seated Cable Row", "back", "all", 3, 4, 4, 10, 10, 12, 90, 20, 40, 60, 12, 24, 36, "full_gym"),
    ("Barbell Bent-Over Row", "back", "all", 3, 4, 4, 8, 8, 10, 90, 20, 40, 60, 12, 24, 36, "full_gym"),
    ("Dumbbell Single-Arm Row", "back", "all", 3, 3, 4, 10, 10, 12, 60, 10, 20, 35, 6, 12, 21, "dumbbells_home"),
    ("T-Bar Row", "back", "intermediate", 0, 3, 4, 0, 8, 10, 90, 0, 30, 50, 0, 18, 30, "full_gym"),
    ("Face Pulls", "back", "all", 3, 3, 4, 12, 15, 15, 60, 10, 20, 30, 6, 12, 18, "full_gym"),
    ("Hyperextensions", "back", "all", 3, 3, 4, 10, 15, 20, 60, 0, 0, 0, 0, 0, 0, "bodyweight_only"),
    ("Resistance Band Row", "back", "beginner", 3, 4, 0, 12, 15, 0, 60, 0, 0, 0, 0, 0, 0, "resistance_bands"),
    ("Barbell Back Squat", "legs", "all", 3, 4, 5, 8, 8, 10, 120, 20, 60, 100, 12, 36, 60, "full_gym"),
    ("Barbell Front Squat", "legs", "intermediate", 0, 3, 4, 0, 8, 8, 120, 0, 40, 80, 0, 24, 48, "full_gym"),
    ("Leg Press", "legs", "all", 3, 4, 4, 10, 10, 12, 90, 40, 100, 180, 24, 60, 108, "full_gym"),
    ("Romanian Deadlift", "legs", "all", 3, 4, 4, 8, 10, 12, 90, 20, 50, 90, 12, 30, 54, "full_gym"),
    ("Lunges (Dumbbell)", "legs", "all", 3, 3, 4, 10, 12, 15, 60, 5, 12, 20, 3, 7, 12, "dumbbells_home"),
    ("Leg Extensions", "legs", "all", 3, 3, 4, 12, 15, 15, 60, 15, 30, 50, 9, 18, 30, "full_gym"),
    ("Lying Leg Curls", "legs", "all", 3, 3, 4, 12, 15, 15, 60, 15, 30, 50, 9, 18, 30, "full_gym"),
    ("Standing Calf Raises", "legs", "all", 3, 4, 4, 15, 20, 25, 60, 20, 40, 70, 12, 24, 42, "full_gym"),
    ("Seated Calf Raises", "legs", "all", 3, 3, 4, 15, 20, 20, 60, 20, 35, 60, 12, 21, 36, "full_gym"),
    ("Bulgarian Split Squat", "legs", "intermediate", 0, 3, 4, 0, 10, 12, 90, 0, 10, 20, 0, 6, 12, "dumbbells_home"),
    ("Goblet Squat", "legs", "all", 3, 3, 4, 10, 12, 15, 60, 10, 20, 32, 6, 12, 19, "kettlebell_home"),
    ("Overhead Barbell Press", "shoulders", "all", 3, 4, 5, 8, 8, 10, 90, 20, 35, 60, 12, 21, 36, "full_gym"),
    ("Seated Dumbbell Press", "shoulders", "all", 3, 3, 4, 8, 10, 12, 90, 8, 15, 25, 5, 9, 15, "dumbbells_home"),
    ("Lateral Raises", "shoulders", "all", 3, 3, 4, 12, 15, 15, 60, 5, 10, 15, 3, 6, 9, "dumbbells_home"),
    ("Front Raises", "shoulders", "all", 3, 3, 4, 12, 15, 15, 60, 5, 10, 15, 3, 6, 9, "dumbbells_home"),
    ("Reverse Pec Deck", "shoulders", "all", 3, 3, 4, 12, 15, 15, 60, 15, 30, 45, 9, 18, 27, "full_gym"),
    ("Arnold Press", "shoulders", "intermediate", 0, 3, 4, 0, 10, 12, 90, 0, 12, 22, 0, 7, 13, "dumbbells_home"),
    ("Upright Row", "shoulders", "all", 3, 3, 4, 10, 12, 12, 60, 15, 30, 45, 9, 18, 27, "full_gym"),
    ("Cable Lateral Raises", "shoulders", "intermediate", 0, 3, 4, 0, 12, 15, 60, 0, 5, 10, 0, 3, 6, "full_gym"),
    ("Shrugs (Dumbbell)", "shoulders", "all", 3, 3, 4, 15, 15, 20, 60, 15, 30, 45, 9, 18, 27, "dumbbells_home"),
    ("Barbell Bicep Curl", "arms", "all", 3, 3, 4, 10, 12, 15, 60, 15, 25, 40, 9, 15, 24, "full_gym"),
    ("Dumbbell Alternate Bicep Curl", "arms", "all", 3, 3, 4, 10, 12, 12, 60, 8, 14, 20, 5, 8, 12, "dumbbells_home"),
    ("Hammer Curls", "arms", "all", 3, 3, 4, 10, 12, 15, 60, 8, 14, 22, 5, 8, 13, "dumbbells_home"),
    ("Tricep Pushdown", "arms", "all", 3, 3, 4, 12, 15, 15, 60, 15, 25, 40, 9, 15, 24, "full_gym"),
    ("Overhead Tricep Extension", "arms", "all", 3, 3, 4, 10, 12, 15, 60, 10, 20, 30, 6, 12, 18, "dumbbells_home"),
    ("Skull Crushers", "arms", "intermediate", 0, 3, 4, 0, 10, 12, 60, 0, 20, 35, 0, 12, 21, "full_gym"),
    ("Tricep Dips", "arms", "all", 3, 3, 4, 8, 15, 20, 60, 0, 0, 0, 0, 0, 0, "bodyweight_only"),
    ("Preacher Curls", "arms", "intermediate", 0, 3, 4, 0, 10, 12, 60, 0, 20, 30, 0, 12, 18, "full_gym"),
]

for ex in strength_exercises:
    add_ex(ex[0], "strength", ex[1], ex[2], ex[3], ex[4], ex[5], ex[6], ex[7], ex[8], ex[9], ex[10], ex[11], ex[12], ex[13], ex[14], ex[15], ex[16], False)


cardio_exercises = [
    ("Running (Treadmill)", "legs", "cardio_machine", True),
    ("Cycling (Stationary)", "legs", "cardio_machine", True),
    ("Rowing Machine", "full_body", "cardio_machine", True),
    ("Elliptical Trainer", "full_body", "cardio_machine", True),
    ("Stair Climber", "legs", "cardio_machine", True),
    ("Jump Rope", "full_body", "bodyweight_only", True),
    ("Jumping Jacks", "full_body", "bodyweight_only", True),
    ("High Knees", "legs", "bodyweight_only", True),
    ("Mountain Climbers (Paced)", "core", "bodyweight_only", True),
    ("Burpees (Paced)", "full_body", "bodyweight_only", False),
    ("Shadow Boxing", "full_body", "bodyweight_only", True),
    ("Swimming (Freestyle)", "full_body", "bodyweight_only", True),
    ("Swimming (Breaststroke)", "full_body", "bodyweight_only", True),
    ("Swimming (Butterfly)", "full_body", "bodyweight_only", True),
    ("Swimming (Backstroke)", "full_body", "bodyweight_only", True),
    ("Walking (Brisk)", "legs", "bodyweight_only", True),
    ("Jogging In Place", "legs", "bodyweight_only", True),
    ("Ski Erg", "full_body", "cardio_machine", True),
    ("Air Bike", "full_body", "cardio_machine", True),
    ("Step Aerobics", "legs", "bodyweight_only", True),
    ("Kickboxing Drills", "full_body", "bodyweight_only", True),
    ("Dancing (Zumba)", "full_body", "bodyweight_only", True),
    ("Agility Ladder Drills", "legs", "bodyweight_only", True),
    ("Speed Skaters (Paced)", "legs", "bodyweight_only", True),
    ("Bear Crawls (Paced)", "full_body", "bodyweight_only", True),
    ("Crab Walks", "full_body", "bodyweight_only", True),
    ("Kettlebell Swings (Light)", "full_body", "kettlebell_home", False),
    ("Punching Bag Work", "arms", "full_gym", True),
    ("Treadmill Incline Walk", "legs", "cardio_machine", True),
    ("Rowing (Water)", "full_body", "bodyweight_only", True),
    ("Jacob's Ladder", "full_body", "cardio_machine", True),
    ("Arm Ergometer", "arms", "cardio_machine", True),
]
for name, m_group, eq, is_timed in cardio_exercises:
    if is_timed:
        add_ex(name, "cardio", m_group, "all", 1, 1, 1, 600, 1200, 1800, 30, 0, 0, 0, 0, 0, 0, eq, True)
    else:
        add_ex(name, "cardio", m_group, "all", 3, 4, 5, 20, 30, 40, 45, 0, 0, 0, 0, 0, 0, eq, False)

hiit_exercises = [
    ("Burpees (Max Effort)", "full_body", "bodyweight_only"),
    ("Mountain Climbers (Sprint)", "core", "bodyweight_only"),
    ("Jump Squats", "legs", "bodyweight_only"),
    ("High Knees (Sprint)", "legs", "bodyweight_only"),
    ("Jumping Lunges", "legs", "bodyweight_only"),
    ("Tuck Jumps", "legs", "bodyweight_only"),
    ("Plank Jacks", "core", "bodyweight_only"),
    ("Skaters (Explosive)", "legs", "bodyweight_only"),
    ("Box Jumps", "legs", "full_gym"),
    ("Battle Ropes", "arms", "full_gym"),
    ("Kettlebell Swings (Heavy)", "glutes", "kettlebell_home"),
    ("Medicine Ball Slams", "full_body", "full_gym"),
    ("Sprint Intervals (Treadmill)", "legs", "cardio_machine"),
    ("Rowing Sprints", "full_body", "cardio_machine"),
    ("Air Bike Sprints", "full_body", "cardio_machine"),
    ("Thrusters (Dumbbell)", "full_body", "dumbbells_home"),
    ("Renegade Rows", "core", "dumbbells_home"),
    ("Push-up to Side Plank", "chest", "bodyweight_only"),
    ("Plyo Push-ups", "chest", "bodyweight_only"),
    ("Bicycle Crunches (Fast)", "core", "bodyweight_only"),
    ("Broad Jumps", "legs", "bodyweight_only"),
    ("Star Jumps", "full_body", "bodyweight_only"),
    ("Suicide Sprints", "legs", "bodyweight_only"),
    ("Agility Cone Drills", "legs", "bodyweight_only"),
    ("Frog Jumps", "legs", "bodyweight_only"),
    ("Bear Crawl Sprints", "full_body", "bodyweight_only"),
    ("Donkey Kicks (Explosive)", "glutes", "bodyweight_only"),
    ("Lunge Chops", "full_body", "dumbbells_home"),
    ("Wall Ball Shots", "full_body", "full_gym"),
    ("Sled Push", "full_body", "full_gym"),
    ("Tire Flips", "full_body", "full_gym"),
    ("Lateral Bound", "legs", "bodyweight_only")
]
for name, m_group, eq in hiit_exercises:
    add_ex(name, "hiit", m_group, "all", 3, 4, 5, 20, 30, 40, 15, 0, 0, 0, 0, 0, 0, eq, True)

yoga_poses = [
    ("Downward-Facing Dog", "full_body", "yoga_mat"),
    ("Upward-Facing Dog", "back", "yoga_mat"),
    ("Chaturanga Dandasana", "chest", "yoga_mat"),
    ("Warrior I", "legs", "yoga_mat"),
    ("Warrior II", "legs", "yoga_mat"),
    ("Warrior III", "legs", "yoga_mat"),
    ("Triangle Pose", "core", "yoga_mat"),
    ("Tree Pose", "legs", "yoga_mat"),
    ("Child's Pose", "back", "yoga_mat"),
    ("Cobra Pose", "back", "yoga_mat"),
    ("Cat Pose", "back", "yoga_mat"),
    ("Cow Pose", "back", "yoga_mat"),
    ("Bridge Pose", "glutes", "yoga_mat"),
    ("Seated Forward Bend", "back", "yoga_mat"),
    ("Pigeon Pose", "glutes", "yoga_mat"),
    ("Camel Pose", "back", "yoga_mat"),
    ("Bow Pose", "back", "yoga_mat"),
    ("Boat Pose", "core", "yoga_mat"),
    ("Crow Pose", "arms", "yoga_mat"),
    ("Eagle Pose", "legs", "yoga_mat"),
    ("Half Moon Pose", "core", "yoga_mat"),
    ("Plank Pose", "core", "yoga_mat"),
    ("Side Plank", "core", "yoga_mat"),
    ("Corpse Pose (Savasana)", "full_body", "yoga_mat"),
    ("Lotus Pose", "legs", "yoga_mat"),
    ("Chair Pose", "legs", "yoga_mat"),
    ("Extended Side Angle", "core", "yoga_mat")
]
for name, m_group, eq in yoga_poses:
    add_ex(name, "yoga", m_group, "all", 1, 2, 3, 30, 45, 60, 15, 0, 0, 0, 0, 0, 0, eq, True)

pilates_exercises = [
    ("The Hundred", "core", "yoga_mat"),
    ("Roll-Up", "core", "yoga_mat"),
    ("Roll-Over", "core", "yoga_mat"),
    ("Single Leg Circle", "legs", "yoga_mat"),
    ("Rolling Like a Ball", "core", "yoga_mat"),
    ("Single Leg Stretch", "core", "yoga_mat"),
    ("Double Leg Stretch", "core", "yoga_mat"),
    ("Spine Stretch Forward", "back", "yoga_mat"),
    ("Open Leg Rocker", "core", "yoga_mat"),
    ("Corkscrew", "core", "yoga_mat"),
    ("Saw", "core", "yoga_mat"),
    ("Swan-Dive", "back", "yoga_mat"),
    ("Single Leg Kick", "glutes", "yoga_mat"),
    ("Double Leg Kick", "back", "yoga_mat"),
    ("Neck Pull", "core", "yoga_mat"),
    ("Scissors", "core", "yoga_mat"),
    ("Bicycle (Pilates)", "core", "yoga_mat"),
    ("Shoulder Bridge", "glutes", "yoga_mat"),
    ("Spine Twist", "core", "yoga_mat"),
    ("Jackknife", "core", "yoga_mat"),
    ("Side Kick", "glutes", "yoga_mat"),
    ("Teaser", "core", "yoga_mat"),
    ("Hip Twist", "core", "yoga_mat"),
    ("Swimming (Pilates)", "back", "yoga_mat"),
    ("Leg Pull Front", "core", "yoga_mat"),
    ("Leg Pull Back", "core", "yoga_mat"),
    ("Kneeling Side Kick", "glutes", "yoga_mat"),
    ("Boomerang", "core", "yoga_mat"),
    ("Seal", "core", "yoga_mat")
]
for name, m_group, eq in pilates_exercises:
    add_ex(name, "pilates", m_group, "all", 2, 3, 4, 30, 45, 60, 20, 0, 0, 0, 0, 0, 0, eq, True)

df = pd.DataFrame(exercises)
output_path = os.path.join(os.path.dirname(__file__), "exercise_database.csv")
df.to_csv(output_path, index=False)

print(f"Exercise database created: {output_path}")
print(df['workout_type'].value_counts())
