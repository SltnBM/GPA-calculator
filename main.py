grade_weights = {
    "A": 4.0,
    "AB": 3.5,
    "B": 3.0,
    "BC": 2.5,
    "C": 2.0,
    "D": 1.0,
    "E": 0.0
}

def calculate_gpa(courses):
    total_credits = 0
    total_weighted_score = 0

    for name, credits, grade in courses:
        weight = grade_weights.get(grade.upper(), None)
        if weight is None:
            print(f"Invalid grade '{grade}' for course {name}. Skipping.")
            continue
        total_credits += credits
        total_weighted_score += credits * weight

    if total_credits == 0:
        return 0.0
    return round(total_weighted_score / total_credits, 2)

def get_category(gpa):
    if gpa >= 3.5:
        return "Excellent"
    elif gpa >= 3.0:
        return "Very Good"
    elif gpa >= 2.5:
        return "Good"
    elif gpa >= 2.0:
        return "Fair"
    else:
        return "Poor"

def main():
    course_list = []
    try:
        num_courses = int(input("How many courses? ").strip())
        if num_courses <= 0:
            print("Number of courses must be at least 1. Exiting.")
            return
    except KeyboardInterrupt:
        print("\nInterrupted before starting. Exiting.")
        return
    except ValueError:
        print("Invalid number. Exiting.")
        return

    for i in range(num_courses):
        try:
            print(f"\nCourse {i+1}")
            name = input("Course name: ").strip()
            while True:
                try:
                    credits_raw = input("Number of credits: ").strip()
                    credits = float(credits_raw)
                    if credits <= 0:
                        print("Credits must be a positive number.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number for credits.")
            while True:
                grade = input("Grade (A, AB, B, BC, C, D, E): ").strip().upper()
                if grade in grade_weights:
                    break
                print("Invalid grade. Please enter one of: A, AB, B, BC, C, D, E.")
            course_list.append((name, credits, grade))
        except KeyboardInterrupt:
            print("\nReceived Ctrl+C, stopping course entry early.")
            break

    gpa = calculate_gpa(course_list)
    print("\n--- Course Summary ---")
    for name, credits, grade in course_list:
        print(f"{name} ({credits} credits) - Grade: {grade}")

    total_credits = sum(credits for _, credits, _ in course_list)
    print(f"\nTotal Credits: {total_credits}")

    print("\nYour GPA is:", gpa)
    print("GPA Category:", get_category(gpa))

if __name__ == "__main__":
    main()
