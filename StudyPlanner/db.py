import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "database",
    "studyplanner.db"
)


def connect_db():
    return sqlite3.connect(DB_PATH)


def create_tables():

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = connect_db()
    cursor = conn.cursor()

    # User table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Task table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            description TEXT,
            priority TEXT,
            deadline TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    # Timetable table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            day TEXT,
            subject TEXT,
            start_time TEXT,
            end_time TEXT
        )
    """)

    # Notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            content TEXT
        )
    """)

    # Progress table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            study_hours REAL,
            topics TEXT
        )
    """)

    conn.commit()
    conn.close()