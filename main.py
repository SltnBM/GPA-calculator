import json
import sys
import os

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt

console = Console()

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
        console.print("\nExiting, [bold red]Good bye.[/]")
        sys.exit(0)

def calculate_gpa(courses):
    total_credits = 0
    total_weighted_score = 0

    for name, credits, grade in courses:
        weight = grade_weights.get(grade.upper(), None)
        if weight is None:
            console.print(f"[yellow]Invalid grade '{grade}' for course {name}. Skipping.[/]")
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

def style_for_grade(grade):
    grade = grade.upper()
    if grade in ("A", "AB"):
        return "bold green"
    if grade in ("B",):
        return "cyan"
    if grade in ("BC", "C"):
        return "yellow"
    if grade in ("D", "E"):
        return "red"
    return ""

def print_summary(course_list):
    gpa = calculate_gpa(course_list)
    console.print("\n[bold underline blue]--- Course Summary ---[/]\n")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Course Name", style="white")
    table.add_column("Credits", justify="right")
    table.add_column("Grade", justify="center")

    for name, credits, grade in course_list:
        table.add_row(name, str(credits), f"[{style_for_grade(grade)}]{grade}[/{style_for_grade(grade)}]")

    total_credits = sum(credits for _, credits, _ in course_list)
    console.print(table)
    console.print(f"[bold]Total Credits:[/] {total_credits}")
    # GPA with colored category
    category = get_category(gpa)
    gpa_style = {
        "Excellent": "bold green",
        "Very Good": "green",
        "Good": "yellow",
        "Fair": "bright_yellow",
        "Poor": "bold red"
    }.get(category, "white")
    console.print(f"[bold]Your GPA is:[/] [{gpa_style}]{gpa}[/{gpa_style}]")
    console.print(f"[bold]GPA Category:[/] [{gpa_style}]{category}[/{gpa_style}]")

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
        console.print(f"[green]Sample template created at '{path}'. You can edit it and rerun.[/]")
    except IOError as e:
        console.print(f"[red]Failed to write template: {e}[/]")

def interactive_input():
    course_list = []
    try:
        num_courses = int(safe_input("How many courses? ").strip())
        if num_courses <= 0:
            console.print("[red]Number of courses must be at least 1. Exiting.[/]")
            return []
    except ValueError:
        console.print("[red]Invalid number. Exiting.[/]")
        return []

    for i in range(num_courses):
        console.print(f"\n[bold]Course {i+1}[/]")
        name = safe_input("Course name: ").strip()
        while True:
            try:
                credits_raw = safe_input("Number of credits: ").strip()
                credits = float(credits_raw)
                if credits <= 0:
                    console.print("[yellow]Credits must be a positive number.[/]")
                    continue
                break
            except ValueError:
                console.print("[yellow]Please enter a valid number for credits.[/]")
        while True:
            grade = safe_input("Grade (A, AB, B, BC, C, D, E): ").strip().upper()
            if grade in grade_weights:
                break
            console.print("[yellow]Invalid grade. Please enter one of: A, AB, B, BC, C, D, E.[/]")
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
                console.print(f"[yellow]Skipping invalid entry: {entry}[/]")
                continue
            courses.append((name, credits, grade))
        return courses
    except FileNotFoundError:
        console.print(f"[red]File not found: {path}[/]")
    except json.JSONDecodeError as e:
        console.print(f"[red]JSON parse error: {e}[/]")
    except IOError as e:
        console.print(f"[red]I/O error reading file: {e}[/]")
    return []

def main():
    console.print("[bold]Choose input method:[/]")
    console.print("1) JSON file")
    console.print("2) Manual input")
    course_list = []

    while True:
        choice = safe_input("Enter 1 or 2: ").strip()
        if choice in ("1", "2"):
            break
        console.print("[yellow]Invalid selection. Please enter 1 or 2.[/]")

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
                    console.print("[blue]Edit the file then run again.[/]")
                    return
            retry = safe_input("Failed to load or no valid entries. Retry? (y/n): ").strip().lower()
            if retry != "y":
                console.print("[blue]Switching to manual input.[/]")
                course_list = interactive_input()
                break
    else:
        course_list = interactive_input()

    if not course_list:
        console.print("[red]No valid courses provided. Exiting.[/]")
        return

    print_summary(course_list)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\nExiting, [bold red]Good bye.[/]")
        sys.exit(0)
