import json
import os
import re
import smtplib
from datetime import date
from email.message import EmailMessage

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "module3_data.json")

STATUSES = ["Not Started", "In Progress", "Completed", "Submitted"]

EXAM_TYPES = [
    "Class Test", "Quiz", "Midterm Exam", "Final Exam", "Lab Exam", "Lab Test",
    "Presentation", "Assignment Deadline", "Project Submission", "Viva",
    "Practical Exam", "Other",
]

EMAIL_SETTINGS = {
    "enabled": False,
    "host": "smtp.gmail.com",
    "port": 587,
    "user": os.environ.get("SMTP_USER", ""),
    "password": os.environ.get("SMTP_PASSWORD", ""),
    "timeout": 10,
}

DEFAULT_REMINDER_DAYS = 2
CLEAR_WORD = "-"
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ------------------------------------------------------------------ Data
def empty_data():
    return {
        "student": {}, "assignments": [], "exams": [], "email_log": [],
        "last_id": {"assignments": 0, "exams": 0},
    }


def load_data():
    if not os.path.exists(DATA_FILE):
        return empty_data()
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            loaded = json.load(f)
        if not isinstance(loaded, dict):
            raise ValueError("file does not contain a JSON object")
    except (ValueError, OSError) as problem:
        backup = DATA_FILE + ".broken"
        try:
            os.replace(DATA_FILE, backup)
            print(f"Data file was damaged ({problem}).")
            print(f"Old file saved as {backup}. Starting with empty data.")
        except OSError:
            print(f"Data file was damaged ({problem}). Starting with empty data.")
        return empty_data()

    for key, value in empty_data().items():
        loaded.setdefault(key, value)
    for kind in ("assignments", "exams"):
        highest = max([item["id"] for item in loaded[kind]], default=0)
        loaded["last_id"][kind] = max(loaded["last_id"].get(kind, 0), highest)
    return loaded


def save_data():
    temp_file = DATA_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(temp_file, DATA_FILE)


def next_id(kind):
    data["last_id"][kind] += 1
    return data["last_id"][kind]


# ------------------------------------------------------------------ Input helpers
def ask_text(prompt, required=True, old=None):
    while True:
        if old and not required:
            shown = f"{prompt} [{old}] ('{CLEAR_WORD}' to clear): "
        elif old:
            shown = f"{prompt} [{old}]: "
        else:
            shown = f"{prompt}: "
        value = input(shown).strip()
        if value == CLEAR_WORD and not required:
            return ""
        if value == "":
            if old:
                return old
            if not required:
                return ""
            print("  This field cannot be empty.")
            continue
        return value


def days_left(date_text):
    return (date.fromisoformat(date_text) - date.today()).days


def ask_date(prompt, old=None, allow_past=True):
    while True:
        text = ask_text(prompt + " (YYYY-MM-DD)", old=old)
        try:
            value = date.fromisoformat(text).isoformat()
        except ValueError:
            print("  Invalid date. Example: 2026-10-25")
            continue
        if not allow_past and text != old and days_left(value) < 0:
            print("  Date cannot be in the past.")
            continue
        return value


def ask_choice(prompt, options, old=None):
    print(prompt)
    for number, option in enumerate(options, start=1):
        print(f"  {number}. {option}")
    old_number = str(options.index(old) + 1) if old in options else None
    while True:
        text = ask_text("Choose number", old=old_number)
        if text.isdecimal() and 1 <= int(text) <= len(options):
            return options[int(text) - 1]
        print("  Invalid choice.")


def ask_int(prompt, old=None, minimum=0):
    while True:
        text = ask_text(prompt, old=None if old is None else str(old))
        if text.isdecimal() and int(text) >= minimum:
            return int(text)
        print(f"  Enter a whole number (at least {minimum}).")


def ask_email(old=None):
    while True:
        value = ask_text("Your email", old=old)
        if EMAIL_PATTERN.match(value):
            return value
        print("  Invalid email. Example: name@gmail.com")


# ------------------------------------------------------------------ Email
def send_email(subject, body):
    to = data["student"]["email"]
    error = ""
    if not EMAIL_SETTINGS["enabled"]:
        print(f"\n  [DEMO EMAIL to {to}]\n  Subject: {subject}\n  " + body.replace("\n", "\n  "))
        status = "Demo"
    else:
        try:
            if not EMAIL_SETTINGS["user"] or not EMAIL_SETTINGS["password"]:
                raise RuntimeError("SMTP_USER / SMTP_PASSWORD environment variable is not set")
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = EMAIL_SETTINGS["user"]
            msg["To"] = to
            msg.set_content(body)
            with smtplib.SMTP(EMAIL_SETTINGS["host"], EMAIL_SETTINGS["port"],
                              timeout=EMAIL_SETTINGS["timeout"]) as server:
                server.starttls()
                server.login(EMAIL_SETTINGS["user"], EMAIL_SETTINGS["password"])
                server.send_message(msg)
            status = "Sent"
        except Exception as problem:
            status, error = "Failed", str(problem)
            print("  Email failed:", problem)

    data["email_log"].append(
        {"date": str(date.today()), "to": to, "subject": subject, "status": status, "error": error}
    )
    return status == "Sent"


def reminder_due(date_text, reminder_days, already_sent):
    left = days_left(date_text)
    return reminder_days > 0 and not already_sent and 0 <= left <= reminder_days


def check_reminders():
    name = data["student"]["name"]
    sent = 0

    for exam in data["exams"]:
        if reminder_due(exam["date"], exam["reminder_days"], exam["reminder_sent"]):
            body = (
                f"Hello {name},\n\nThis is a reminder for your upcoming assessment.\n\n"
                f"Course: {exam['course']}\nAssessment Type: {exam['type']}\n"
                f"Title: {exam['title']}\nDate: {exam['date']}\n"
                f"Time: {exam['time'] or '-'}\nRoom Number: {exam['room'] or '-'}\n"
            )
            if exam.get("description"):
                body += f"Details: {exam['description']}\n"
            if send_email(f"Reminder: {exam['title']} on {exam['date']}", body):
                exam["reminder_sent"] = True
                sent += 1

    for item in data["assignments"]:
        not_submitted = item["status"] != "Submitted"
        days = item.get("reminder_days", DEFAULT_REMINDER_DAYS)
        if not_submitted and reminder_due(item["deadline"], days, item["reminder_sent"]):
            body = (
                f"Hello {name},\n\nYour assignment deadline is coming up.\n\n"
                f"Course: {item['course']}\nAssignment: {item['title']}\n"
                f"Deadline: {item['deadline']}\nStatus: {item['status']}\n"
            )
            if item.get("description"):
                body += f"Details: {item['description']}\n"
            if send_email(f"Assignment due soon: {item['title']}", body):
                item["reminder_sent"] = True
                sent += 1

    save_data()
    print(f"Reminder check done. Emails sent: {sent}")
    if not EMAIL_SETTINGS["enabled"]:
        print("(Demo mode is on: no real email is sent.)")


# ------------------------------------------------------------------ Shared helpers
def find_by_id(items, label):
    text = input(f"Enter {label} id: ").strip()
    for item in items:
        if str(item["id"]) == text:
            return item
    print("  Not found.")
    return None


def delete_item(items, label):
    item = find_by_id(items, label)
    if item is None:
        return
    if input("Delete? (y/n): ").strip().lower() == "y":
        items.remove(item)
        save_data()
        print("Deleted.")
    else:
        print("Cancelled.")


# ------------------------------------------------------------------ Assignments
def add_assignment():
    print("\n--- Add Assignment ---")
    course = ask_text("Course name")
    title = ask_text("Assignment title")
    description = ask_text("Description (optional)", required=False)
    deadline = ask_date("Deadline", allow_past=False)
    reminder_days = ask_int("Remind how many days before? (0 = no reminder)",
                            old=DEFAULT_REMINDER_DAYS)
    data["assignments"].append({
        "id": next_id("assignments"), "course": course, "title": title,
        "description": description, "assigned_date": str(date.today()),
        "deadline": deadline, "status": "Not Started",
        "reminder_days": reminder_days, "reminder_sent": False,
    })
    save_data()
    print("Assignment added.")


def show_assignments():
    print("\n--- My Assignments ---")
    if not data["assignments"]:
        print("No assignments yet.")
        return
    for item in sorted(data["assignments"], key=lambda a: a["deadline"]):
        late = "  (OVERDUE)" if item["status"] != "Submitted" and days_left(item["deadline"]) < 0 else ""
        print(f"[{item['id']}] {item['course']} | {item['title']} | "
              f"Given: {item.get('assigned_date', '-')} | Deadline: {item['deadline']} | "
              f"{item['status']}{late}")
        if item.get("description"):
            print(f"     Note: {item['description']}")


def advance_status():
    item = find_by_id(data["assignments"], "assignment")
    if item is None:
        return
    position = STATUSES.index(item["status"]) if item["status"] in STATUSES else -1
    if position == len(STATUSES) - 1:
        print("Already submitted.")
        return
    item["status"] = STATUSES[position + 1]
    save_data()
    print("Status changed to:", item["status"])


def edit_assignment():
    item = find_by_id(data["assignments"], "assignment")
    if item is None:
        return
    print("Press Enter to keep the current value.")
    course = ask_text("Course name", old=item["course"])
    title = ask_text("Title", old=item["title"])
    description = ask_text("Description", required=False, old=item["description"])
    deadline = ask_date("Deadline", old=item["deadline"], allow_past=False)
    reminder_days = ask_int("Remind how many days before? (0 = no reminder)",
                            old=item.get("reminder_days", DEFAULT_REMINDER_DAYS))
    status = ask_choice("Status:", STATUSES, old=item["status"])

    # deadline বা reminder দিন বদলালে আবার reminder যাবে
    if deadline != item["deadline"] or reminder_days != item.get("reminder_days"):
        item["reminder_sent"] = False
    item.update({"course": course, "title": title, "description": description,
                 "deadline": deadline, "reminder_days": reminder_days, "status": status})
    save_data()
    print("Assignment updated.")


def assignment_menu():
    while True:
        print("\n=== Assignments ===")
        print("1. Add  2. View  3. Next status step  4. Edit  5. Delete  0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_assignment()
        elif choice == "2":
            show_assignments()
        elif choice == "3":
            advance_status()
        elif choice == "4":
            edit_assignment()
        elif choice == "5":
            delete_item(data["assignments"], "assignment")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


# ------------------------------------------------------------------ Exams
def ask_exam_details(old=None):
    old = old or {}
    exam_type = ask_choice("Assessment type:", EXAM_TYPES, old=old.get("type_choice"))
    if exam_type == "Other":
        label = ask_text("Write your assessment type", old=old.get("type"))
    else:
        label = exam_type
    return {
        "course": ask_text("Course name", old=old.get("course")),
        "type_choice": exam_type,
        "type": label,
        "title": ask_text("Title", old=old.get("title")),
        "date": ask_date("Date", old=old.get("date"), allow_past=False),
        "time": ask_text("Time, e.g. 10:00 AM (optional)", required=False, old=old.get("time")),
        "room": ask_text("Room number (optional)", required=False, old=old.get("room")),
        "description": ask_text("Description (optional)", required=False, old=old.get("description")),
        "reminder_days": ask_int("Remind how many days before? (0 = no reminder)",
                                 old=old.get("reminder_days", DEFAULT_REMINDER_DAYS)),
    }


def add_exam():
    print("\n--- Add Exam / Assessment ---")
    exam = ask_exam_details()
    exam["id"] = next_id("exams")
    exam["reminder_sent"] = False
    data["exams"].append(exam)
    save_data()
    print("Exam added.")


def edit_exam():
    exam = find_by_id(data["exams"], "exam")
    if exam is None:
        return
    print("Press Enter to keep the current value.")
    updated = ask_exam_details(old=exam)
    # তারিখ বা reminder দিন বদলালে আবার reminder যাবে
    if updated["date"] != exam["date"] or updated["reminder_days"] != exam["reminder_days"]:
        exam["reminder_sent"] = False
    exam.update(updated)
    save_data()
    print("Exam updated.")


def show_exams():
    when = ask_choice("Show which exams?", ["Upcoming", "Past"])
    type_filter = ask_choice("Filter by type:", ["All types"] + EXAM_TYPES)
    sort_order = ask_choice("Sort by date:", ["Earliest first", "Latest first"])

    result = []
    for exam in data["exams"]:
        is_upcoming = days_left(exam["date"]) >= 0
        if (when == "Upcoming") != is_upcoming:
            continue
        if type_filter != "All types" and exam["type_choice"] != type_filter:
            continue
        result.append(exam)

    result.sort(key=lambda e: e["date"], reverse=(sort_order == "Latest first"))

    print(f"\n--- {when} Exams ({len(result)}) ---")
    if not result:
        print("No exams found.")
    for e in result:
        moment = f"{e['date']} {e['time']}".strip()
        print(f"[{e['id']}] {moment} | {e['course']} | "
              f"{e['type']} | {e['title']} | Room: {e['room'] or '-'}")
        if e.get("description"):
            print(f"     Note: {e['description']}")


def exam_menu():
    while True:
        print("\n=== Exams & Assessments ===")
        print("1. Add  2. View  3. Edit  4. Delete  0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_exam()
        elif choice == "2":
            show_exams()
        elif choice == "3":
            edit_exam()
        elif choice == "4":
            delete_item(data["exams"], "exam")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


# ------------------------------------------------------------------ Main
def show_email_log():
    print("\n--- Email Log ---")
    if not data["email_log"]:
        print("No emails yet.")
    for entry in data["email_log"]:
        line = f"{entry['date']} | {entry['to']} | {entry['subject']} | {entry['status']}"
        if entry.get("error"):
            line += f" | Error: {entry['error']}"
        print(line)


def edit_profile():
    print("\n--- My Profile --- (Press Enter to keep the current value)")
    data["student"]["name"] = ask_text("Your name", old=data["student"]["name"])
    data["student"]["email"] = ask_email(old=data["student"]["email"])
    save_data()
    print("Profile updated.")


def main():
    if not data["student"]:
        print("First time setup")
        data["student"] = {"name": ask_text("Your name"), "email": ask_email()}
        save_data()

    print(f"\nWelcome, {data['student']['name']}!")
    check_reminders()  # প্রোগ্রাম চালু হলেই reminder দেখে নেয়

    while True:
        print("\n===== Student Assistance: Assignments & Exams =====")
        print("1. Assignments  2. Exams  3. Send due reminders now  4. Email log  "
              "5. My profile  0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            assignment_menu()
        elif choice == "2":
            exam_menu()
        elif choice == "3":
            check_reminders()
        elif choice == "4":
            show_email_log()
        elif choice == "5":
            edit_profile()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


data = empty_data()

if __name__ == "__main__":
    data = load_data()
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
