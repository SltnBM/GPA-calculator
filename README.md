# 🎓 GPA Calculator CLI
A simple Python CLI tool to calculate GPA (IPK) based on course credits (SKS) and grades, with support for early exit via `Ctrl+C`.

## ✨ Features
- 📝 Input course name, SKS (credits), and grade (A, AB, B, BC, C, D, E)
- ➗ Weighted GPA calculation based on SKS
- 🏷️ GPA classification: Excellent / Very Good / Good / Fair / Poor
- ❌ Early exit with `Ctrl+C` showing partial summary
- ⚡ Lightweight CLI, zero external dependencies

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
   - For each course: name, SKS (can be decimal), and grade
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
```bash
How many courses? 3

Course 1
Course name: Calculus
Number of credits (SKS): 3
Grade (A, AB, B, BC, C, D, E): A

Course 2
Course name: Algorithm
Number of credits (SKS): 4
Grade (A, AB, B, BC, C, D, E): B

Course 3
Course name: Database
Number of credits (SKS): 2
Grade (A, AB, B, BC, C, D, E): AB

--- Course Summary ---
Calculus (3.0 SKS) - Grade: A
Algorithm (4.0 SKS) - Grade: B
Database (2.0 SKS) - Grade: AB

Your GPA is: 3.35
GPA Category: Very Good
```

## 🤝 Contributing
Feel free to open issues or submit pull requests for improvements or bug fixes.

## 📬 Connect With Me
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sultan%20Badra-blue?logo=linkedin\&logoColor=white\&style=flat-square)](https://www.linkedin.com/in/sultan-badra)

## 📜 License
Feel Free to use, modify, and share for personal and educational purposes.