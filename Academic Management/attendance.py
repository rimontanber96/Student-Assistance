from database import get_connection


# Calculate Attendance Percentage
def calculate_attendance(student_id, course_id):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    SELECT
        COUNT(*),
        SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END)
    FROM attendance
    WHERE student_id = %s
    AND course_id = %s
    """

    try:
        cursor.execute(sql, (student_id, course_id))
        total_classes, attended_classes = cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

    if total_classes == 0:
        return None          # no classes yet

    percentage = (int(attended_classes) / total_classes) * 100

    return round(percentage, 2)


# Check Attendance Warning
def check_attendance_warning(student_id, course_id):
    percentage = calculate_attendance(student_id, course_id)

    if percentage is None:
        return "No classes recorded yet."

    if percentage < 75:
        return "WARNING: Attendance below 75%!"

    return "Attendance is satisfactory."