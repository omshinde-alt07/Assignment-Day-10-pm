from student_analytics import *

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