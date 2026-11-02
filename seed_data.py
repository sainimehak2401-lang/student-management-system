
import random
import pandas as pd
from pathlib import Path

random.seed(42)

FIRST_NAMES = [
    "Aarav", "Aanya", "Aditya", "Ananya", "Arjun",
    "Diya", "Ishaan", "Isha", "Kabir", "Kiara",
    "Krish", "Meera", "Mohit", "Neha", "Riya",
    "Rahul", "Simran", "Sanya", "Vivaan", "Zoya",
    "Karan", "Nisha", "Aman", "Priya", "Dev",
]

LAST_NAMES = [
    "Sharma", "Verma", "Singh", "Kumar", "Gupta",
    "Patel", "Kaur", "Malhotra", "Mehta", "Joshi",
    "Saini", "Yadav", "Chopra", "Das", "Reddy",
]

SUBJECTS = ["Python", "DBMS", "Computer Networks", "Mathematics", "Operating Systems"]

students = []

for i in range(1, 101):
    name = f"{FIRST_NAMES[(i - 1) % len(FIRST_NAMES)]} {LAST_NAMES[(i * 3) % len(LAST_NAMES)]}"

    marks = {
        subject: random.randint(25, 100)
        for subject in SUBJECTS
    }

    total_obtained = sum(marks.values())
    total_maximum = len(SUBJECTS) * 100
    percentage = round(total_obtained / total_maximum * 100, 2)

    students.append({
        "student_id": f"STU{i:03d}",
        "name": name,
        "email": f"student{i:03d}@example.com",
        "course": random.choice(["BCA", "BBA", "B.Tech"]),
        "semester": random.randint(1, 8),
        "attendance": random.randint(55, 100),
        **{f"{subject}_marks": score for subject, score in marks.items()},
        "total_marks": total_obtained,
        "maximum_marks": total_maximum,
        "percentage": percentage,
        "result": "PASS" if all(score >= 40 for score in marks.values()) else "FAIL",
    })

df = pd.DataFrame(students)

output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

df.to_csv(output_dir / "students.csv", index=False)

print("100 demo student records created successfully!")
print(f"File saved to: {output_dir / 'students.csv'}")
print(df.head(5).to_string(index=False))
