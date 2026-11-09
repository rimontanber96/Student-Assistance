from database import get_connection


# Calculate Letter Grade and Grade Point
def calculate_grade(marks):
    if marks >= 80:
        return "A+", 4.00
    elif marks >= 75:
        return "A", 3.75
    elif marks >= 70:
        return "A-", 3.50
    elif marks >= 65:
        return "B+", 3.25
    elif marks >= 60:
        return "B", 3.00
    elif marks >= 55:
        return "B-", 2.75
    elif marks >= 50:
        return "C+", 2.50
    elif marks >= 45:
        return "C", 2.25
    elif marks >= 40:
        return "D", 2.00
    else:
        return "F", 0.00


# Add Grade
def add_grade(student_id, course_id, marks, semester):
    if not 0 <= marks <= 100:
        raise ValueError("Marks must be between 0 and 100.")

    if semester < 1:
        raise ValueError("Semester must be 1 or more.")

    grade, grade_point = calculate_grade(marks)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        sql = """
        INSERT INTO grades
        (student_id, course_id, marks, grade, grade_point, semester)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (student_id, course_id, marks, grade, grade_point, semester)
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


# View Grades
def view_grades():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM grades")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


# Used by SGPA and CGPA: total (grade point x credit) / total credit
def get_gpa(student_id, semester=None):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    SELECT SUM(g.grade_point * c.credit),
           SUM(c.credit)
    FROM grades g
    JOIN courses c ON g.course_id = c.course_id
    WHERE g.student_id = %s
    """
    values = [student_id]

    if semester is not None:
        sql += " AND g.semester = %s"
        values.append(semester)

    try:
        cursor.execute(sql, values)
        total_points, total_credits = cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

    if not total_credits:
        return 0.00

    return round(float(total_points) / float(total_credits), 2)


# Calculate SGPA (one semester)
def calculate_sgpa(student_id, semester):
    return get_gpa(student_id, semester)


# Calculate CGPA (all semesters)
def calculate_cgpa(student_id):
    return get_gpa(student_id)