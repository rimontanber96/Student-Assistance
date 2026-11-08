import hashlib
import os

from db import connect_db


def hash_password(password, salt=None):

    if salt is None:
        salt = os.urandom(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )

    return salt.hex() + ":" + hashed.hex()


def register():

    username = input("Enter username: ")
    password = input("Enter password: ")

    hashed = hash_password(password)

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )

        conn.commit()
        conn.close()

        print("Registration successful!")

    except Exception:
        print("Username already exists!")


def login():

    username = input("Username: ")
    password = input("Password: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:

        stored_salt, stored_hash = user[1].split(":")

        entered_hash = hash_password(
            password,
            bytes.fromhex(stored_salt)
        )

        if entered_hash == user[1]:
            print("Login successful!")
            return user[0]

    print("Invalid username or password!")
    return None