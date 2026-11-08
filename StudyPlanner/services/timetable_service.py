from db import connect_db


def add_timetable(user_id):

    day = input("Day: ")
    subject = input("Subject: ")
    start = input("Start time: ")
    end = input("End time: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO timetable
        (user_id, day, subject, start_time, end_time)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, day, subject, start, end))

    conn.commit()
    conn.close()

    print("Timetable added!")


def view_timetable(user_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM timetable
        WHERE user_id = ?
        ORDER BY day, start_time
    """, (user_id,))

    records = cursor.fetchall()
    conn.close()

    for item in records:
        print(
            item[2], "|",
            item[3], "|",
            item[4], "-", item[5]
        )