# Grade to weight mapping
grade_weights = {
    "A": 8,
    "AB": 7,
    "B": 6,
    "BC": 5,
    "C": 4,
    "D": 2,
    "E": 0
}

# Function to calculate GPA
def calculate_gpa(courses):
    total_credits = 0
    total_weighted_score = 0

    for course in courses:
        name, credits, grade = course
        weight = grade_weights.get(grade.upper(), None)
        if weight is None:
            print(f"Invalid grade '{grade}' for course {name}. Skipping.")
            continue
        total_credits += credits
        total_weighted_score += credits * weight

    if total_credits == 0:
        return 0.0
    return round(total_weighted_score / total_credits, 2)

course_list = [
    ("Mathematics", 3, "A"),
    ("Programming", 4, "AB"),
    ("Networking", 2, "B"),
    ("Database", 3, "BC"),
]

gpa = calculate_gpa(course_list)
print("Your GPA is:", gpa)
