from db import connect_db


def add_note(user_id):

    title = input("Note title: ")
    content = input("Write your note: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notes (user_id, title, content)
        VALUES (?, ?, ?)
    """, (user_id, title, content))

    conn.commit()
    conn.close()

    print("Note saved!")


def view_notes(user_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM notes WHERE user_id = ?",
        (user_id,)
    )

    notes = cursor.fetchall()
    conn.close()

    for note in notes:
        print("\nTitle:", note[2])
        print("Content:", note[3])