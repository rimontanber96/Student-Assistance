"""ডাটাবেস, নিরাপত্তা ও ইমেইল: সব সহায়ক কাজ এক ফাইলে।"""

import hashlib
import os
import re
import secrets
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

import mysql.connector

# ---------- সেটিংস (নিজের মান local_config.py-তে দাও) ----------
DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME = "localhost", 3306, "root", "", "student_assistance"
EMAIL_MODE = "console"          # "console" = টার্মিনালে ছাপে, "smtp" = আসল ইমেইল
SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD = "smtp.gmail.com", 587, "", ""
CODE_VALID_MINUTES = 15
try:
    from local_config import *  # noqa: F401,F403  (ওপরের মান বদলে দেয়)
except ImportError:
    pass


# ---------- ডাটাবেস: সব SQL এই চার ফাংশন দিয়ে যায় ----------
# মান বসাতে সবসময় %s ব্যবহার করবে, স্ট্রিং জুড়ে SQL বানালে SQL injection হয়।

def _run(sql, params, how):
    con = mysql.connector.connect(host=DB_HOST, port=DB_PORT, user=DB_USER,
                                  password=DB_PASSWORD, database=DB_NAME)
    try:
        cur = con.cursor(dictionary=True)      # সারি পাই row["username"] রূপে
        cur.execute(sql, params)
        if how == "one":
            return cur.fetchone()
        if how == "all":
            return cur.fetchall()
        con.commit()
        return cur.lastrowid if how == "insert" else cur.rowcount
    finally:
        con.close()                            # error হলেও কানেকশন বন্ধ


def one(sql, params=()):      return _run(sql, params, "one")       # একটা সারি
def many(sql, params=()):     return _run(sql, params, "all")       # সব সারি
def execute(sql, params=()):  return _run(sql, params, "rows")      # UPDATE/DELETE
def insert(sql, params=()):   return _run(sql, params, "insert")    # নতুন id ফেরত


# ---------- নিরাপত্তা ----------

def hash_password(password, salt=None):
    """পাসওয়ার্ড + র‍্যান্ডম salt মিশিয়ে ২ লক্ষবার হ্যাশ করে (digest, salt) ফেরত দেয়"""
    salt = salt or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000).hex()
    return digest, salt


def check_password(password, digest, salt):
    return secrets.compare_digest(hash_password(password, salt)[0], digest)


def password_problem(password):
    """দুর্বল হলে কারণ (টেক্সট), ঠিক থাকলে None"""
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return "Password needs both letters and digits"
    return None


def valid_email(email):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None


def new_code():
    """(৬ সংখ্যার কোড, মেয়াদ শেষের সময়)"""
    return f"{secrets.randbelow(10**6):06d}", datetime.now() + timedelta(minutes=CODE_VALID_MINUTES)


# ---------- ইমেইল ----------

def send_email(to, subject, body):
    if EMAIL_MODE == "console":
        print(f"\n--- EMAIL to {to} ---\nSubject: {subject}\n{body}\n--------------------")
        return
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = subject, SMTP_USER, to
    msg.set_content(body)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()                      # সংযোগ এনক্রিপ্ট করে
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
