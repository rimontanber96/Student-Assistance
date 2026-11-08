from db import connect_db


def add_task(user_id):

    title = input("Task title: ")
    description = input("Description: ")
    priority = input("Priority (Low/Medium/High): ")
    deadline = input("Deadline (YYYY-MM-DD): ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (user_id, title, description, priority, deadline)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, title, description, priority, deadline))

    conn.commit()
    conn.close()

    print("Task added successfully!")


def view_tasks(user_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE user_id = ?",
        (user_id,)
    )

    tasks = cursor.fetchall()
    conn.close()

    for task in tasks:
        print("\nID:", task[0])
        print("Title:", task[2])
        print("Description:", task[3])
        print("Priority:", task[4])
        print("Deadline:", task[5])
        print("Completed:", task[6])


def complete_task(user_id):

    task_id = input("Enter Task ID: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = 1
        WHERE id = ? AND user_id = ?
    """, (task_id, user_id))

    conn.commit()

    if cursor.rowcount:
        print("Task completed!")
    else:
        print("Task not found!")

    conn.close()