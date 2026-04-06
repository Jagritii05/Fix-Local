"""
A small student grades calculator — with intentional bugs for testing the debug session.
"""

def calculate_average(grades):
    """Calculate the average of a list of grades."""
    total = 0
    for grade in grades:
        total += grade
    average = total / len(grades)  # BUG: will crash on empty list (ZeroDivisionError)
    return average


def get_letter_grade(score):
    """Convert a numeric score to a letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    # BUG: missing else — returns None for scores below 60


def process_students(student_data):
    """Process a dictionary of students and their grades."""
    results = {}
    for name, grades in student_data.items():
        avg = calculate_average(grades)
        letter = get_letter_grade(avg)
        results[name] = {
            "average": round(avg, 2),
            "letter": letter,
            "passed": letter != "F"  # BUG: letter is None for <60, so this is always True
        }
    return results


def main():
    students = {
        "Alice": [85, 92, 78, 90],
        "Bob": [55, 42, 38, 50],
        "Charlie": [],               # BUG trigger: empty list will crash calculate_average
        "Diana": [91, 88, 95, 87],
    }

    results = process_students(students)

    for name, info in results.items():
        print(f"{name}: Average = {info['average']}, Grade = {info['letter']}, Passed = {info['passed']}")


if __name__ == "__main__":
    main()
