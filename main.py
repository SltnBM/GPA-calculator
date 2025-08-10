import json, sys, os, csv
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()
grade_weights = {"A": 4.0, "AB": 3.5, "B": 3.0, "BC": 2.5, "C": 2.0, "D": 1.0, "E": 0.0}

def safe_input(prompt):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        console.print("\nExiting, [bold red]Good bye.[/]")
        sys.exit(0)

def calculate_gpa(courses):
    total_credits = total_score = 0
    for name, credits, grade in courses:
        weight = grade_weights.get(grade.upper())
        if weight is None:
            console.print(f"[yellow]Invalid grade '{grade}' for course {name}. Skipping.[/]")
            continue
        total_credits += credits
        total_score += credits * weight
    return round(total_score / total_credits, 2) if total_credits else 0.0

def get_category(gpa):
    return ("Excellent" if gpa >= 3.5 else
            "Very Good" if gpa >= 3.0 else
            "Good" if gpa >= 2.5 else
            "Fair" if gpa >= 2.0 else "Poor")

def style_for_grade(grade):
    return ("bold green" if grade in ("A", "AB") else
            "cyan" if grade == "B" else
            "yellow" if grade in ("BC", "C") else
            "red" if grade in ("D", "E") else "")

def print_summary(course_list):
    gpa = calculate_gpa(course_list)
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Course Name", style="white")
    table.add_column("Credits", justify="right")
    table.add_column("Grade", justify="center")
    for name, credits, grade in course_list:
        style = style_for_grade(grade)
        table.add_row(name, str(credits), f"[{style}]{grade}[/{style}]")
    total_credits = sum(c for _, c, _ in course_list)
    category = get_category(gpa)
    gpa_style = {"Excellent": "bold green", "Very Good": "green", "Good": "yellow",
                 "Fair": "bright_yellow", "Poor": "bold red"}.get(category, "white")
    console.print("\n[bold underline blue]--- Course Summary ---[/]\n")
    console.print(table)
    console.print(f"[bold]Total Credits:[/] {total_credits}")
    console.print(f"[bold]Your GPA is:[/] [{gpa_style}]{gpa}[/{gpa_style}]")
    console.print(f"[bold]GPA Category:[/] [{gpa_style}]{category}[/{gpa_style}]")
    return {"gpa": gpa, "category": category, "total_credits": total_credits}

def export_results(course_list, summary, dest_path, fmt):
    data = {
        "generated_at": datetime.now().isoformat(),
        "total_credits": summary["total_credits"],
        "gpa": summary["gpa"],
        "category": summary["category"],
        "courses": [{"name": n, "credits": c, "grade": g} for n, c, g in course_list]
    }
    try:
        if fmt in ("json", "both"):
            with open(dest_path if fmt == "json" else os.path.splitext(dest_path)[0]+".json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            if fmt == "json": console.print(f"[green]Exported summary to JSON file: {dest_path}[/]")
        if fmt in ("txt", "both"):
            with open(dest_path if fmt == "txt" else os.path.splitext(dest_path)[0]+".txt", "w", encoding="utf-8") as f:
                f.write("=== Course Summary ===\n")
                for c in data["courses"]:
                    f.write(f"{c['name']} | Credits: {c['credits']} | Grade: {c['grade']}\n")
                f.write(f"\nTotal Credits: {data['total_credits']}\nGPA: {data['gpa']}\nCategory: {data['category']}\nGenerated at: {data['generated_at']}\n")
            if fmt == "txt": console.print(f"[green]Exported summary to TXT file: {dest_path}[/]")
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
    while True:
        raw = safe_input("How many courses?: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= max_courses:
            num_courses = int(raw)
            break
        console.print("[yellow]Enter a valid number between 1 and {max_courses}.[/]")
    course_list = []
    for i in range(num_courses):
        console.print(f"\n[bold]Course {i+1}[/]")
        name = safe_input("Course name: ").strip()
        while not name:
            console.print("[yellow]Course name cannot be empty.[/]")
            name = safe_input("Course name: ").strip()
        while True:
            try:
                credits = float(safe_input("Number of credits: ").strip())
                if credits > 0: break
                console.print("[yellow]Credits must be positive.[/]")
            except ValueError:
                console.print("[yellow]Please enter a valid number.[/]")
        while True:
            grade = safe_input("Grade (A, AB, B, BC, C, D, E): ").strip().upper()
            if grade in grade_weights: break
            console.print("[yellow]Invalid grade.[/]")
        course_list.append((name, credits, grade))
    return course_list

def load_from_file(path, filetype):
    try:
        with open(path, "r", encoding="utf-8") as f:
            rows = json.load(f) if filetype == "json" else list(csv.DictReader(f))
        courses = []
        for r in rows:
            name = r.get("name", "").strip()
            try: credits = float(r.get("credits", 0))
            except: credits = -1
            grade = r.get("grade", "").strip().upper()
            if name and credits > 0 and grade in grade_weights:
                courses.append((name, credits, grade))
            else:
                console.print(f"[yellow]Skipping invalid entry: {r}[/]")
        return courses
    except FileNotFoundError:
        console.print(f"[red]File not found: {path}[/]")
    except (json.JSONDecodeError, IOError) as e:
        console.print(f"[red]File error: {e}[/]")
    return []

def choose_input_method():
    console.print("[bold]Choose input method:[/]\n1) JSON file\n2) Manual input\n3) CSV file")
    while True:
        choice = safe_input("Enter 1/2/3: ").strip()
        if choice in ("1", "2", "3"): return choice
        console.print("[yellow]Invalid selection.[/]")

def process_input(choice):
    if choice == "1":
        while True:
            path = safe_input("Path to JSON file: ").strip()
            courses = load_from_file(path, "json")
            if courses: return courses
            if not os.path.exists(path) and safe_input(f"File '{path}' not found. Create sample template here? (y/n): ").strip().lower() == "y":
                create_json_template(path)
                console.print("[blue]Edit the file then run again.[/]")
                sys.exit(0)
            if safe_input("Retry? (y/n): ").strip().lower() != "y":
                console.print("[blue]Switching to manual input.[/]")
                return interactive_input()
    elif choice == "2":
        return interactive_input()
    elif choice == "3":
        while True:
            path = safe_input("Path to CSV file: ").strip()
            courses = load_from_file(path, "csv")
            if courses: return courses
            if safe_input("Retry? (y/n): ").strip().lower() != "y":
                console.print("[blue]Switching to manual input.[/]")
                return interactive_input()

def main():
    while True:
        multi = ""
        while multi not in ("y", "n"):
            console.print("[bold]===== GPA CALCULATOR =====[/]\n[bold]Do you want to calculate for multiple semesters?[/]")
            multi = safe_input("Multiple semesters? (y/n): ").strip().lower()
        all_courses, semester_summaries = [], []
        if multi == "y":
            while True:
                raw = safe_input("How many semesters?: ").strip()
                if raw.isdigit() and int(raw) > 0:
                    num_semesters = int(raw)
                    break
                console.print("[yellow]Enter a valid number greater than 0.[/]")
            for s in range(num_semesters):
                console.print(f"\n[bold underline green]=== Semester {s+1} ===[/]")
                courses = process_input(choose_input_method())
                if not courses:
                    console.print(f"[red]Semester {s+1} has no valid courses. Skipping.[/]")
                    continue
                summary = print_summary(courses)
                semester_summaries.append(summary)
                all_courses.extend(courses)
        else:
            courses = process_input(choose_input_method())
            if not courses:
                console.print("[red]No valid courses provided. Exiting.[/]")
                return
            summary = print_summary(courses)
            semester_summaries.append(summary)
            all_courses.extend(courses)
        ipk = 0
        if len(semester_summaries) > 1:
            total_weight = sum(s["gpa"] * s["total_credits"] for s in semester_summaries)
            total_credits = sum(s["total_credits"] for s in semester_summaries)
            ipk = round(total_weight / total_credits, 2) if total_credits else 0.0
            gpa_style = {"Excellent": "bold green", "Very Good": "green", "Good": "yellow",
                         "Fair": "bright_yellow", "Poor": "bold red"}.get(get_category(ipk), "white")
            console.print("\n[bold underline blue]--- Final Summary ---[/]")
            console.print(f"[bold]Your IPK is:[/] [{gpa_style}]{ipk}[/{gpa_style}]")
        export = safe_input("\nSave result to file? (y/n): ").strip().lower()
        if export == "y":
            fmt = ""
            while fmt not in ("txt", "json", "both"):
                fmt = safe_input("Format (txt/json/both): ").strip().lower()
            default_name = "gpa_summary" if fmt == "both" else f"gpa_summary.{fmt}"
            path = safe_input(f"Destination file [{default_name}]: ").strip() or default_name
            export_results(all_courses,
                {"gpa": ipk if len(semester_summaries) > 1 else semester_summaries[0]["gpa"],
                 "category": get_category(ipk if len(semester_summaries) > 1 else semester_summaries[0]["gpa"]),
                 "total_credits": sum(s["total_credits"] for s in semester_summaries)},
                path, fmt)
        if safe_input("\nDo you want to input another GPA calculation? (y/n): ").strip().lower() != "y":
            console.print("[bold green]Thank you. Goodbye![/]")
            break

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print("\nExiting, [bold red]Good bye.[/]")
        sys.exit(0)
