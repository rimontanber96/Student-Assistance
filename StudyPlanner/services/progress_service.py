from db import connect_db


def add_progress(user_id):

    hours = float(input("Study hours: "))
    topics = input("Topics covered: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO progress (user_id, study_hours, topics)
        VALUES (?, ?, ?)
    """, (user_id, hours, topics))

    conn.commit()
    conn.close()

    print("Study progress saved!")


def view_progress(user_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT study_hours, topics
        FROM progress
        WHERE user_id = ?
    """, (user_id,))

    records = cursor.fetchall()
    conn.close()

    total_hours = 0

    for item in records:

        print("\nStudy hours:", item[0])
        print("Topics:", item[1])

        total_hours += item[0]

    print("\nTotal study hours:", total_hours)