# 🎓 GPA Calculator CLI
A simple Python CLI tool to calculate GPA based on course credits and grades.

## ✨ Features
- 📝 Input course name, credits, and grade (A, AB, B, BC, C, D, E)
- ➗ Weighted GPA calculation based on course credits
- 🏷️ GPA classification: Excellent / Very Good / Good / Fair / Poor
- 📚 Support for multiple semesters with per-semester GPA summary
- 💾 Export results to `.txt` or `.json` or both (`.txt` & `.json`)
- 🔁 Option to calculate GPA again without exiting the program
- 📈 Auto-calculates final cumulative GPA if multiple semesters are entered
- 🧠 Supports different input methods (manual or JSON) for each semester
- 🧾 Auto-create sample JSON file if input file is missing
- 🛡️ Input validation for missing, invalid, or incorrect grade/credit formats
- 🌈 Beautiful colored output with tables and styled GPA categories using `rich`
- ❌ Early exit with `Ctrl+C` showing partial summary
- ⚡ Lightweight CLI, zero external dependencies

## 📋 Requirements
1. 🐍 Python 3.6+
2. 📦 `Rich` for styled console output

Install dependencies by running either:
```bash
pip install -r requirements.txt
```

or manually
```bash
pip install rich
```

## 🚀 How to Use
1. 📥 Clone the repository
```bash
https://github.com/SltnBM/GPA-calculator.git
```
2. 📂 Navigate to the project directory
```bash
cd GPA-calculator
```
3. ▶️ Run the script
```bash
python main.py
```
4. 🖊️ Follow prompts:
   - Enter number of courses
   - For each course: name, credits (can be decimal), and grade
   - Press `Ctrl+C` at any time to stop early and still get the summary

## 📊 Grade Scale
| Grade | Weight |
|-------|--------|
| A     | 4.0    |
| AB    | 3.5    |
| B     | 3.0    |
| BC    | 2.5    |
| C     | 2.0    |
| D     | 1.0    |
| E     | 0.0    |

## 💻 Example Session
===== GPA CALCULATOR =====
Do you want to calculate for multiple semesters?
Multiple semesters? (y/n): n
```bash
Choose input method:
1) JSON file
2) Manual input
Enter 1 or 2: 2        
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

## 📄 Using JSON Template
Instead of manual input, you can use a JSON file like the example above to calculate your GPA automatically.

1️⃣ **Edit the Template**  
A ready-to-use `courses.json` file is already provided in the repository. You can edit it to match your own courses, credits, and grades.

2️⃣ **Run the Script** 
   ```bash
   python main.py
   ```

3️⃣ **Choose JSON Option** 
   ```bash
   Choose input method:
   1) JSON file
   2) Manual input
   Enter 1 or 2: 1
   Path to JSON file: courses.json
   ```

4️⃣ **Get Results**  
If the file is valid, the program will read the data and display the GPA summary immediately.

💡 **Tips**:
- 🆓 The file name can be anything, as long as it ends with `.json` and follows the correct format.
- ⚠️ If the file doesn’t exist, the program will offer to create a sample template for you.
- 🎯 Grades must be one of: `A`, `AB`, `B`, `BC`, `C`, `D`, `E` (case-insensitive).

## 📂 Example JSON Template
```json
[
  { "name": "Calculus", "credits": 3, "grade": "A" },
  { "name": "Physics", "credits": 4, "grade": "BC" },
  { "name": "Programming Fundamentals", "credits": 3, "grade": "AB" }
]
```

## 🎯 GPA Classification

The following table shows the numeric ranges used to classify the calculated GPA:

| Category  | GPA Range (inclusive) |
| --------- | --------------------- |
| Excellent | 3.75 – 4.00           |
| Very Good | 3.25 – 3.74           |
| Good      | 2.50 – 3.24           |
| Fair      | 2.00 – 2.49           |
| Poor      | 0.00 – 1.99           |

> **Note:** GPA is calculated based on weighted credits. The classification is determined using the actual GPA value before rounding, to ensure accuracy.

## 🤝 Contributing
Feel free to open issues or submit pull requests for improvements or bug fixes.

## 📬 Connect With Me
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sultan%20Badra-blue?logo=linkedin\&logoColor=white\&style=flat-square)](https://www.linkedin.com/in/sultan-badra)

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
