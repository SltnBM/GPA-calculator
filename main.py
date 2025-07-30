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

course_list = []
num_courses = int(input("How many courses? "))

for i in range(num_courses):
    print(f"\nCourse {i+1}")
    name = input("Course name: ")
    credits = int(input("Number of credits (SKS): "))
    grade = input("Grade (A, AB, B, BC, C, D, E): ")
    course_list.append((name, credits, grade))

gpa = calculate_gpa(course_list)
print("\nYour GPA is:", gpa)
