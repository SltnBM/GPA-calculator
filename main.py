import json
import sys
import os

grade_weights = {
    "A": 4.0,
    "AB": 3.5,
    "B": 3.0,
    "BC": 2.5,
    "C": 2.0,
    "D": 1.0,
    "E": 0.0
}

def safe_input(prompt):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\nExiting, Good bye.")
        sys.exit(0)

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

def print_summary(course_list):
    gpa = calculate_gpa(course_list)
    print("\n--- Course Summary ---")
    for name, credits, grade in course_list:
        print(f"{name} ({credits} credits) - Grade: {grade}")
    total_credits = sum(credits for _, credits, _ in course_list)
    print(f"\nTotal Credits: {total_credits}")
    print("Your GPA is:", gpa)
    print("GPA Category:", get_category(gpa))

def create_json_template(path):
    sample = [
        { "name": "Calculus", "credits": 3, "grade": "A" },
        { "name": "Physics", "credits": 4, "grade": "BC" },
        { "name": "English Literature", "credits": 2, "grade": "B" },
        { "name": "Programming Fundamentals", "credits": 3, "grade": "AB" }
    ]
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sample, f, indent=2)
        print(f"Sample template created at '{path}'. You can edit it and rerun.")
    except IOError as e:
        print(f"Failed to write template: {e}")

def interactive_input():
    course_list = []
    try:
        num_courses = int(safe_input("How many courses? ").strip())
        if num_courses <= 0:
            print("Number of courses must be at least 1. Exiting.")
            return []
    except ValueError:
        print("Invalid number. Exiting.")
        return []

    for i in range(num_courses):
        print(f"\nCourse {i+1}")
        name = safe_input("Course name: ").strip()
        while True:
            try:
                credits_raw = safe_input("Number of credits: ").strip()
                credits = float(credits_raw)
                if credits <= 0:
                    print("Credits must be a positive number.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number for credits.")
        while True:
            grade = safe_input("Grade (A, AB, B, BC, C, D, E): ").strip().upper()
            if grade in grade_weights:
                break
            print("Invalid grade. Please enter one of: A, AB, B, BC, C, D, E.")
        course_list.append((name, credits, grade))

    return course_list

def load_from_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        courses = []
        for entry in raw:
            name = entry.get("name", "").strip()
            try:
                credits = float(entry.get("credits", 0))
            except (TypeError, ValueError):
                credits = -1
            grade = entry.get("grade", "").strip().upper()
            if not name or credits <= 0 or grade not in grade_weights:
                print(f"Skipping invalid entry: {entry}")
                continue
            courses.append((name, credits, grade))
        return courses
    except FileNotFoundError:
        print(f"File not found: {path}")
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
    except IOError as e:
        print(f"I/O error reading file: {e}")
    return []

def main():
    print("Choose input method:")
    print("1) JSON file")
    print("2) Manual input")
    course_list = []

    while True:
        choice = safe_input("Enter 1 or 2: ").strip()
        if choice in ("1", "2"):
            break
        print("Invalid selection. Please enter 1 or 2.")

    if choice == "1":
        while True:
            path = safe_input("Path to JSON file: ").strip()
            course_list = load_from_json_file(path)
            if course_list:
                break
            if not os.path.exists(path):
                create = safe_input(f"File '{path}' not found. Create sample template here? (y/n): ").strip().lower()
                if create == "y":
                    create_json_template(path)
                    print("Edit the file then run again.")
                    return
            retry = safe_input("Failed to load or no valid entries. Retry? (y/n): ").strip().lower()
            if retry != "y":
                print("Switching to manual input.")
                course_list = interactive_input()
                break
    else:
        course_list = interactive_input()

    if not course_list:
        print("No valid courses provided. Exiting.")
        return

    print_summary(course_list)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting, Good bye.")
        sys.exit(0)
