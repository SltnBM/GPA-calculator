import json
import sys
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.text import Text
import csv

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
    return {
        "gpa": gpa,
        "category": category,
        "total_credits": total_credits
    }

def export_results(course_list, summary, dest_path, fmt):
    data = {
        "generated_at": datetime.now().isoformat(),
        "total_credits": summary["total_credits"],
        "gpa": summary["gpa"],
        "category": summary["category"],
        "courses": [
            {"name": name, "credits": credits, "grade": grade}
            for name, credits, grade in course_list
        ]
    }
    try:
        if fmt == "json":
            with open(dest_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            console.print(f"[green]Exported summary to JSON file: {dest_path}[/]")

        elif fmt == "txt":
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write("=== Course Summary ===\n")
                for c in data["courses"]:
                    f.write(f"{c['name']} | Credits: {c['credits']} | Grade: {c['grade']}\n")
                f.write(f"\nTotal Credits: {data['total_credits']}\n")
                f.write(f"GPA: {data['gpa']}\n")
                f.write(f"Category: {data['category']}\n")
                f.write(f"Generated at: {data['generated_at']}\n")
            console.print(f"[green]Exported summary to TXT file: {dest_path}[/]")

        elif fmt == "both":
            base = os.path.splitext(dest_path)[0]
            for ext in ("json", "txt"):
                export_results(course_list, summary, f"{base}.{ext}", ext)

    except IOError as e:
        console.print(f"[red]Failed to export: {e}[/]")


def create_json_template(path):
    sample = [
        {"name": "Calculus", "credits": 3, "grade": "A"},
        {"name": "Physics", "credits": 4, "grade": "BC"},
        {"name": "English Literature", "credits": 2, "grade": "B"},
        {"name": "Programming Fundamentals", "credits": 3, "grade": "AB"}
    ]
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sample, f, indent=2)
        console.print(f"[green]Sample template created at '{path}'. You can edit it and rerun.[/]")
    except IOError as e:
        console.print(f"[red]Failed to write template: {e}[/]")

def interactive_input(max_courses=100):
    course_list = []
    while True:
        raw = safe_input(f"How many courses?: ").strip()
        if not raw:
            console.print("[yellow]Please enter a number.[/]")
            continue
        try:
            num_courses = int(raw)
            if num_courses < 1 or num_courses > max_courses:
                console.print(f"[yellow]Enter a number between 1 and {max_courses}.[/]")
                continue
            break
        except ValueError:
            console.print("[yellow]Invalid number. Please enter an number.[/]")

    for i in range(num_courses):
        console.print(f"\n[bold]Course {i+1}[/]")
        name = safe_input("Course name: ").strip()
        while not name:
            console.print("[yellow]Course name cannot be empty.[/]")
            name = safe_input("Course name: ").strip()

        while True:
            credits_raw = safe_input("Number of credits: ").strip()
            try:
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

def load_from_csv_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            courses = []
            for row in reader:
                name = row.get("name", "").strip()
                try:
                    credits = float(row.get("credits", 0))
                except (TypeError, ValueError):
                    credits = -1
                grade = row.get("grade", "").strip().upper()
                if not name or credits <= 0 or grade not in grade_weights:
                    console.print(f"[yellow]Skipping invalid entry: {row}[/]")
                    continue
                courses.append((name, credits, grade))
            return courses
    except FileNotFoundError:
        console.print(f"[red]File not found: {path}[/]")
    except IOError as e:
        console.print(f"[red]I/O error reading file: {e}[/]")
    return []

def main():
    while True:
        multi = ""
        while multi not in ("y", "n"):
            console.print("[bold]===== GPA CALCULATOR =====[/]")
            console.print("[bold]Do you want to calculate for multiple semesters?[/]")
            multi = safe_input("Multiple semesters? (y/n): ").strip().lower()
            if not multi:
                console.print("[yellow]Input cannot be empty. Please enter 'y' or 'n'.[/]")
            elif multi not in ("y", "n"):
                console.print("[yellow]Invalid input. Please enter 'y' or 'n'.[/]")


        all_courses = []
        semester_summaries = []

        if multi == "y":
            while True:
                raw = safe_input("How many semesters?: ").strip()
                if not raw.isdigit() or int(raw) <= 0:
                    console.print("[yellow]Enter a valid number greater than 0.[/]")
                    continue
                num_semesters = int(raw)
                break

            for s in range(num_semesters):
                console.print(f"\n[bold underline green]=== Semester {s+1} ===[/]")
                console.print("[bold]Choose input method:[/]")
                console.print("1) JSON file")
                console.print("2) Manual input")
                console.print("3) CSV file")
                course_list = []

                while True:
                    choice = safe_input("Enter 1/2/3:").strip()
                    if choice in ("1", "2", "3"):
                        break
                    console.print("[yellow]Invalid selection. Please enter 1/2/3.[/]")

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
                elif choice == "2":
                    course_list = interactive_input()
                elif choice == "3":
                    while True:
                        path = safe_input("Path to CSV file: ").strip()
                        course_list = load_from_csv_file(path)
                        if course_list:
                            break
                        retry = safe_input("Failed to load or no valid entries. Retry? (y/n): ").strip().lower()
                        if retry != "y":
                            console.print("[blue]Switching to manual input.[/]")
                            course_list = interactive_input()
                            break
                else:
                    course_list = interactive_input()

                if not course_list:
                    console.print(f"[red]Semester {s+1} has no valid courses. Skipping.[/]")
                    continue

                summary = print_summary(course_list)
                semester_summaries.append(summary)
                all_courses.extend(course_list)
        else:
            console.print("\n[bold]Choose input method:[/]")
            console.print("1) JSON file")
            console.print("2) Manual input")
            console.print("3) CSV file")

            course_list = []
            while True:
                choice = safe_input("Enter 1/2/3: ").strip()
                if choice in ("1", "2", "3"):
                    break
                console.print("[yellow]Invalid selection. Please enter 1/2/3.[/]")

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
            elif choice == "2":
                course_list = interactive_input()
            elif choice == "3":
                while True:
                    path = safe_input("Path to CSV file: ").strip()
                    course_list = load_from_csv_file(path)
                    if course_list:
                        break
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

            summary = print_summary(course_list)
            semester_summaries.append(summary)
            all_courses.extend(course_list)

        if len(semester_summaries) > 1:
            total_weight = sum(s["gpa"] * s["total_credits"] for s in semester_summaries)
            total_credits = sum(s["total_credits"] for s in semester_summaries)
            ipk = round(total_weight / total_credits, 2) if total_credits > 0 else 0.0
            console.print("\n[bold underline blue]--- Final Summary ---[/]")
            gpa_style = {
                "Excellent": "bold green",
                "Very Good": "green",
                "Good": "yellow",
                "Fair": "bright_yellow",
                "Poor": "bold red"
            }.get(get_category(ipk), "white")
            console.print(f"[bold]Your IPK is:[/] [{gpa_style}]{ipk}[/{gpa_style}]")

        export = safe_input("\nSave result to file? (y/n): ").strip().lower()
        if export == "y":
            fmt = ""
            while fmt not in ("txt", "json", "both"):
                fmt = safe_input("Format (txt/json/both): ").strip().lower()

            default_name = "gpa_summary" if fmt == "both" else f"gpa_summary.{fmt}"
            path = safe_input(f"Destination file [{default_name}]: ").strip()
            if not path:
                path = default_name
            export_results(
                all_courses,
                {
                    "gpa": ipk if len(semester_summaries) > 1 else semester_summaries[0]["gpa"],
                    "category": get_category(ipk if len(semester_summaries) > 1 else semester_summaries[0]["gpa"]),
                    "total_credits": sum(s["total_credits"] for s in semester_summaries)
                },
                path,
                fmt
            )

        again = safe_input("\nDo you want to input another GPA calculation? (y/n): ").strip().lower()
        if again != "y":
            console.print("[bold green]Thank you. Goodbye![/]")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\nExiting, [bold red]Good bye.[/]")
        sys.exit(0)