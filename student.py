from typing import List, Dict, Any
from collections import defaultdict


def create_student(name: str, roll: str, **marks: int) -> Dict[str, Any]:
    if not name or not roll:
        raise ValueError("Name and roll cannot be empty")

    if not marks:
        raise ValueError("At least one subject mark must be provided")

    for subject, score in marks.items():
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            raise ValueError(f"Invalid mark for {subject}")

    return {
        "name": name,
        "roll": roll,
        "marks": marks,
        "attendance": 0.0
    }


def calculate_gpa(*marks: float, scale: float = 10.0) -> float:

    if not marks:
        raise ValueError("Marks cannot be empty")

    if scale <= 0:
        raise ValueError("Scale must be positive")

    for m in marks:
        if m < 0 or m > 100:
            raise ValueError("Marks must be between 0 and 100")

    avg = sum(marks) / len(marks)
    return round((avg / 100) * scale, 2)


def get_top_performers(
    students: List[Dict],
    n: int = 5,
    subject: str = None
) -> List[Dict]:


    if not students:
        return []

    if n <= 0:
        return []

    def avg_marks(student):
        marks = student.get("marks", {})
        if not marks:
            return 0
        return sum(marks.values()) / len(marks)

    if subject:
        sorted_students = sorted(
            students,
            key=lambda x: x.get("marks", {}).get(subject, 0),
            reverse=True
        )
    else:
        sorted_students = sorted(
            students,
            key=avg_marks,
            reverse=True
        )

    return sorted_students[:n]


def generate_report(student: Dict, **options) -> str:
    if not student:
        return "Invalid student data"

    include_rank = options.get("include_rank", True)
    include_grade = options.get("include_grade", True)
    verbose = options.get("verbose", False)

    marks = student.get("marks", {})
    avg = sum(marks.values()) / len(marks) if marks else 0

    grade = None
    if include_grade:
        if avg >= 90:
            grade = "A"
        elif avg >= 75:
            grade = "B"
        elif avg >= 60:
            grade = "C"
        else:
            grade = "D"

    report = f"Student: {student['name']} ({student['roll']})\n"
    report += f"Average: {round(avg,2)}\n"

    if include_grade:
        report += f"Grade: {grade}\n"

    if verbose:
        report += f"Marks: {marks}\n"
        report += f"Attendance: {student.get('attendance',0)}\n"

    if include_rank:
        report += "Rank: N/A\n"

    return report


def classify_students(students: List[Dict]) -> Dict[str, List]:

    result = defaultdict(list)

    if not students:
        return {"A": [], "B": [], "C": [], "D": []}

    for s in students:
        marks = s.get("marks", {})
        if not marks:
            result["D"].append(s)
            continue

        avg = sum(marks.values()) / len(marks)

        if avg >= 90:
            result["A"].append(s)
        elif avg >= 75:
            result["B"].append(s)
        elif avg >= 60:
            result["C"].append(s)
        else:
            result["D"].append(s)

    return dict(result)

s1 = create_student("Amit", "R001", math=85, python=92, ml=78)
s2 = create_student("Priya", "R002", math=95, python=88, ml=91)
s3 = create_student("Rahul", "R003", math=60, python=65, ml=70)

students = [s1, s2, s3]

assert s1["name"] == "Amit"
assert "math" in s1["marks"]
assert s1["roll"] == "R001"

assert calculate_gpa(85, 92, 78) == 8.5
assert calculate_gpa(100, 100) == 10.0
assert calculate_gpa(50, 50, scale=5) == 2.5

top1 = get_top_performers(students, n=1)
assert top1[0]["name"] == "Priya"

top_python = get_top_performers(students, n=1, subject="python")
assert top_python[0]["marks"]["python"] == 92

assert len(get_top_performers(students, n=2)) == 2
report = generate_report(s1)
assert "Amit" in report

report_verbose = generate_report(s1, verbose=True)
assert "Marks" in report_verbose

report_no_grade = generate_report(s1, include_grade=False)
assert "Grade" not in report_no_grade

classification = classify_students(students)

assert isinstance(classification, dict)
assert "A" in classification
assert any(s["name"] == "Priya" for s in classification["A"])