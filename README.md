# GPA Calculator CLI
A simple Python CLI tool to calculate GPA based on course credits and grades.

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="120" style="border:0" alt="Python Logo">
</p>

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)
![Requirements](https://img.shields.io/badge/requirements-rich%20v13%2B-green)
![Repo Size](https://img.shields.io/github/repo-size/SltnBM/GPA-calculator)

---

## Features
- Flexible input: manual, JSON, or CSV (per semester) with auto JSON sample.
- Validation for missing/invalid grades & credits.
- Weighted GPA calculation + classification.
- Multi-semester support with per-semester & cumulative GPA.
- Export to TXT, JSON, CSV, or all formats.
- Colorful table output using Rich.
- Recalculate without restart, graceful exit with partial summary.

---

## Requirements
1. Python 3.6+
2. `Rich` package

Install dependencies by running either:
```bash
pip install -r requirements.txt
```

or manually
```bash
pip install rich
```

---

## Project Structure
```plaintext
GPA-calculator/
├── LICENSE
├── README.md
├── courses.json
├── main.py
└── requirements.txt
```

---

## How to Use
1. Make sure you have Python installed (Python 3.6 or higher recommended). Download it from [python.org](https://www.python.org/downloads/).  
2. Clone the repository
```bash
git clone https://github.com/SltnBM/GPA-calculator.git
```
3. Navigate to the project directory
```bash
cd GPA-calculator
```
4. Run the script
```bash
python main.py
```
5. Follow prompts:
   - Enter number of courses
   - For each course: name, credits (can be decimal), and grade
   - Press `Ctrl+C` at any time to stop early and still get the summary

---

## Example Session
```bash
===== GPA CALCULATOR =====
Do you want to calculate for multiple semesters?
Multiple semesters? (y/n): n
Choose input method:
1) JSON file
2) Manual input
3) CSV file
Enter 1/2/3: 2        
How many courses? 3

Course 1
Course name: Calculus
Number of credits: 3
Grade (A, AB, B, BC, C, D, E): A

Course 2
Course name: Algorithm
Number of credits: 4
Grade (A, AB, B, BC, C, D, E): B

Course 3
Course name: Database
Number of credits: 2
Grade (A, AB, B, BC, C, D, E): AB

--- Course Summary ---

┏━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━┓
┃ Course Name ┃ Credits ┃ Grade ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━┩
│ Calculus    │     3.0 │   A   │
│ Algorithm   │     4.0 │   B   │
│ Database    │     2.0 │  AB   │
└─────────────┴─────────┴───────┘
Total Credits: 9.0
Your GPA is: 3.44
GPA Category: Very Good

Save result to file? (y/n): y
Format (txt/json): txt
Destination file [gpa_summary.txt]: gpa_summary_example.txt
Exported summary to TXT file: gpa_summary_example.txt
```

---

## Using JSON Template
Instead of manual input, you can use a JSON file like the example above to calculate your GPA automatically.

1️. **Edit the Template**  

A ready-to-use `courses.json` file is already provided in the repository. You can edit it to match your own courses, credits, and grades.

2️. **Run the Script** 
   ```bash
   python main.py
   ```

3️. **Choose JSON Option** 
   ```bash
   Choose input method:
   1) JSON file
   2) Manual input
   Enter 1 or 2: 1
   Path to JSON file: courses.json
   ```

4️. **Get Results**  
If the file is valid, the program will read the data and display the GPA summary immediately.

**Tips**:
- The file name can be anything, as long as it ends with `.json` and follows the correct format.
- If the file doesn’t exist, the program will offer to create a sample template for you.
- Grades must be one of: `A`, `AB`, `B`, `BC`, `C`, `D`, `E` (case-insensitive).

### Example JSON Template
```json
[
  { "name": "Calculus", "credits": 3, "grade": "A" },
  { "name": "Physics", "credits": 4, "grade": "BC" },
  { "name": "Programming Fundamentals", "credits": 3, "grade": "AB" }
]
```

---

## Using CSV Template
Instead of manual input, you can use a CSV file like the example above to calculate your GPA automatically.

1️. **Edit the Template**

A ready-to-use `template_courses.csv` file is provided in the repository. You can edit it to match your own courses, credits, and grades.

2️. **Run the Script** 
   ```bash
   python main.py
   ```

3️. **Choose CSV Options**
```bash
Choose input method:
1) JSON file
2) Manual input
3) CSV file
Enter 1, 2, or 3: 3
Path to CSV file: template_courses.csv
```

**Tips**:
- CSV must have the exact column names: name, credits, grade.
- The file name can be anything, as long as it ends with `.csv` and follows the correct format.
- Credits can be decimal values.
- Grades must be one of: `A`, `AB`, `B`, `BC`, `C`, `D`, `E` (case-insensitive).

### Example CSV Template
```csv
name,credits,grade
Calculus,3,A
Physics,4,BC
English Literature,2,B
Programming Fundamentals,3,AB
Database Systems,3,A
Statistics,2,C
```

---

## Grade Scale
| Grade | Weight |
|-------|--------|
| A     | 4.0    |
| AB    | 3.5    |
| B     | 3.0    |
| BC    | 2.5    |
| C     | 2.0    |
| D     | 1.0    |
| E     | 0.0    |

---

## GPA Classification
The following table shows the numeric ranges used to classify the calculated GPA:

| Category  | GPA Range (inclusive) |
| --------- | --------------------- |
| Excellent | 3.75 – 4.00           |
| Very Good | 3.25 – 3.74           |
| Good      | 2.50 – 3.24           |
| Fair      | 2.00 – 2.49           |
| Poor      | 0.00 – 1.99           |

> **Note:** GPA is calculated based on weighted credits. The classification is determined using the actual GPA value before rounding, to ensure accuracy.

---

## Calculation Formula
**Grade weights:** `A=4.0, AB=3.5, B=3.0, BC=2.5, C=2.0, D=1.0, E=0.0` (case-insensitive).
**Semester GPA**
```
GPA = round( Σ (grade_weight × credits) / Σ credits , 2 )
```

**Cumulative GPA**
```
IPK = round( Σ (GPA_semester × semester_credits) / Σ semester_credits , 2 )
```

---

## Contributing
Feel free to open issues or submit pull requests for improvements or bug fixes.

---

## Connect With Me
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sultan%20Badra-blue?logo=linkedin\&logoColor=white\&style=flat-square)](https://www.linkedin.com/in/sultan-badra)

---

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
