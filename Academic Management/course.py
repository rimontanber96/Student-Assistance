from database import get_connection


def check_course(course_code, course_name, credit):
    if not course_code.strip() or not course_name.strip():
        raise ValueError("Course code and name cannot be empty.")

    if not 0 < credit <= 9:
        raise ValueError("Credit must be between 0 and 9.")


def add_course(course_code, course_name, credit):
    check_course(course_code, course_name, credit)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        sql = """
        INSERT INTO courses (course_code, course_name, credit)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (course_code.strip(), course_name.strip(), credit))
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def view_courses():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM courses")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def update_course(course_id, course_code, course_name, credit):
    check_course(course_code, course_name, credit)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        sql = """
        UPDATE courses
        SET course_code = %s,
            course_name = %s,
            credit = %s
        WHERE course_id = %s
        """
        cursor.execute(
            sql,
            (course_code.strip(), course_name.strip(), credit, course_id)
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


# Grades and attendance of this course are deleted automatically
# (ON DELETE CASCADE in the SQL files).
def delete_course(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
        connection.commit()
    finally:
        cursor.close()
        connection.close()