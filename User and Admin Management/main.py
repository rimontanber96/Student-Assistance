"""Student Assistance: মেম্বার ১ (User ও Admin Management)
চালাও:  python main.py

ফাইলের গঠন: (১) লজিক: নিয়ম ও ডাটাবেসের কাজ, (২) মেনু: ইনপুট ও আউটপুট, (৩) মূল লুপ।
লজিকের ফাংশনে print/input নেই, নিয়ম ভাঙলে ValueError দেয়; মেনু সেটা ধরে বার্তা দেখায়।"""

import getpass
import secrets
import sys
from datetime import datetime

import db

current_user = None     # এখন কে লগইন করা আছে (None মানে কেউ না)


# =============================== (১) লজিক ===============================

def get_or_create(table, name, parent_col=None, parent_id=None):
    """নাম আগে থেকে থাকলে তার id দেয়, না থাকলে নতুন বানিয়ে id দেয়"""
    if parent_col:
        row = db.one(f"SELECT id FROM {table} WHERE name=%s AND {parent_col}=%s", (name, parent_id))
        return row["id"] if row else db.insert(
            f"INSERT INTO {table}({parent_col}, name) VALUES(%s,%s)", (parent_id, name))
    row = db.one(f"SELECT id FROM {table} WHERE name=%s", (name,))
    return row["id"] if row else db.insert(f"INSERT INTO {table}(name) VALUES(%s)", (name,))


def academic_ids(uni, dept, intake, section):
    """টাইপ করা নাম থেকে (university, department, intake, section)-এর id; ফাঁকা হলে None"""
    uni, dept, intake, section = (x.strip() for x in (uni, dept, intake, section))
    u = get_or_create("universities", uni) if uni else None
    d = get_or_create("departments", dept, "university_id", u) if u and dept else None
    i = get_or_create("intakes", intake, "department_id", d) if d and intake else None
    s = get_or_create("sections", section, "intake_id", i) if i and section else None
    return u, d, i, s


def academic_names(user_id):
    r = db.one(
        "SELECT u.name AS uni, d.name AS dept, i.name AS intake, s.name AS section FROM users x "
        "LEFT JOIN universities u ON u.id=x.university_id LEFT JOIN departments d ON d.id=x.department_id "
        "LEFT JOIN intakes i ON i.id=x.intake_id LEFT JOIN sections s ON s.id=x.section_id "
        "WHERE x.id=%s", (user_id,))
    return [r[k] or "" for k in ("uni", "dept", "intake", "section")]


def send_code(user_id, email, purpose):
    """৬ সংখ্যার কোড বানিয়ে ডাটাবেসে রাখে ও ইমেইলে পাঠায় (purpose: verify বা reset)"""
    code, expires = db.new_code()
    db.execute("UPDATE users SET code=%s, code_purpose=%s, code_expires=%s WHERE id=%s",
               (code, purpose, expires, user_id))
    what = "verify your account" if purpose == "verify" else "reset your password"
    db.send_email(email, "Student Assistance code",
                  f"Use this code to {what}: {code}\n(valid for {db.CODE_VALID_MINUTES} minutes)")


def check_code(email, code, purpose):
    """কোড ঠিক, উদ্দেশ্য মেলে ও মেয়াদ বাকি থাকলে ইউজারের সারি দেয়, নইলে ValueError"""
    u = db.one("SELECT id, code, code_purpose, code_expires FROM users WHERE email=%s",
               (email.strip().lower(),))
    ok = (u and u["code"] and u["code_purpose"] == purpose and u["code_expires"]
          and u["code_expires"] > datetime.now()
          and secrets.compare_digest(u["code"].encode(), code.strip().encode()))
    if not ok:
        raise ValueError("Wrong or expired code")
    return u


def register(username, email, password, student_id, uni, dept, intake, section):
    username, email = username.strip(), email.strip().lower()
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters")
    if not db.valid_email(email):
        raise ValueError("Invalid email address")
    problem = db.password_problem(password)
    if problem:
        raise ValueError(problem)
    if db.one("SELECT id FROM users WHERE username=%s OR email=%s", (username, email)):
        raise ValueError("Username or email already used")
    digest, salt = db.hash_password(password)
    user_id = db.insert(
        "INSERT INTO users(username,email,password_hash,salt,student_id,"
        "university_id,department_id,intake_id,section_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (username, email, digest, salt, student_id.strip() or None, *academic_ids(uni, dept, intake, section)))
    send_code(user_id, email, "verify")      # is_active ডিফল্টে 0, ভেরিফাই না করা পর্যন্ত লগইন বন্ধ


def resend_code(email):
    u = db.one("SELECT id, is_active FROM users WHERE email=%s", (email.strip().lower(),))
    if u and not u["is_active"]:
        send_code(u["id"], email.strip().lower(), "verify")


def verify(email, code):
    u = check_code(email, code, "verify")
    db.execute("UPDATE users SET is_active=1, code=NULL, code_purpose=NULL, code_expires=NULL WHERE id=%s",
               (u["id"],))


def login(username, password):
    global current_user
    u = db.one("SELECT * FROM users WHERE username=%s", (username.strip(),))
    if not u or not db.check_password(password, u["password_hash"], u["salt"]):
        raise ValueError("Wrong username or password")   # দুই ভুলে একই বার্তা
    if not u["is_active"]:
        raise ValueError("Please verify your email first")
    current_user = u


def logout():
    global current_user
    current_user = None


def request_reset(email):
    u = db.one("SELECT id FROM users WHERE email=%s", (email.strip().lower(),))
    if u:                                    # ইমেইল আছে কি না, তা ব্যবহারকারীকে জানানো হয় না
        send_code(u["id"], email.strip().lower(), "reset")


def set_password(user_id, new_password):
    problem = db.password_problem(new_password)
    if problem:
        raise ValueError(problem)
    digest, salt = db.hash_password(new_password)
    db.execute("UPDATE users SET password_hash=%s, salt=%s, code=NULL, code_purpose=NULL, "
               "code_expires=NULL WHERE id=%s", (digest, salt, user_id))


def reset_password(email, code, new_password):
    u = check_code(email, code, "reset")
    set_password(u["id"], new_password)


def change_password(old_password, new_password):
    if not db.check_password(old_password, current_user["password_hash"], current_user["salt"]):
        raise ValueError("Old password is wrong")
    set_password(current_user["id"], new_password)


def update_profile(full_name, student_id, birthday, uni, dept, intake, section):
    """role এখানে বদলায় না, তাই ছাত্র নিজেকে Admin বানাতে পারে না"""
    global current_user
    if birthday:
        try:
            birthday = datetime.strptime(birthday, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Birthday must be like 2003-05-21")
    db.execute(
        "UPDATE users SET full_name=%s, student_id=%s, birthday=%s, university_id=%s, "
        "department_id=%s, intake_id=%s, section_id=%s WHERE id=%s",
        (full_name or None, student_id or None, birthday or None,
         *academic_ids(uni, dept, intake, section), current_user["id"]))
    current_user = db.one("SELECT * FROM users WHERE id=%s", (current_user["id"],))


def require_admin():
    """অ্যাডমিনের প্রতিটা কাজের শুরুতে চলে (মেনুতে বাটন না দেখানোর পরেও দ্বিতীয় পাহারা)"""
    if not current_user or current_user["role"] != "admin":
        raise ValueError("Admins only")


def not_self(user_id):
    if user_id == current_user["id"]:
        raise ValueError("You cannot do this to your own account")


def admin_users():
    require_admin()
    return db.many("SELECT id, username, email, role, is_active FROM users ORDER BY id")


def admin_set_active(user_id, flag):
    require_admin(); not_self(user_id)
    db.execute("UPDATE users SET is_active=%s WHERE id=%s", (1 if flag else 0, user_id))


def admin_set_role(user_id, role):
    require_admin(); not_self(user_id)
    if role not in ("student", "admin"):
        raise ValueError("Role must be student or admin")
    db.execute("UPDATE users SET role=%s WHERE id=%s", (role, user_id))


def admin_delete_user(user_id):
    require_admin(); not_self(user_id)
    db.execute("DELETE FROM users WHERE id=%s", (user_id,))


# রিপোর্ট করা কনটেন্ট: মেম্বার ৪-এর টেবিল লাগবে, নাম মিলিয়ে নাও:
#   resources(id, title)    resource_reports(id, resource_id, reason)
def admin_reports():
    """মেম্বার ৪-এর টেবিল না থাকলে None, তাই তাদের কাজ না এলেও এটা ক্র্যাশ করে না"""
    require_admin()
    if not (db.one("SHOW TABLES LIKE %s", ("resource_reports",)) and db.one("SHOW TABLES LIKE %s", ("resources",))):
        return None
    return db.many("SELECT r.id, r.resource_id, res.title, r.reason FROM resource_reports r "
                   "JOIN resources res ON res.id = r.resource_id ORDER BY r.id DESC")


def admin_report_action(report_id, delete_resource):
    require_admin()
    r = db.one("SELECT resource_id FROM resource_reports WHERE id=%s", (report_id,))
    if not r:
        raise ValueError("Report not found")
    if delete_resource:       # আপত্তিকর ফাইল ও তার সব রিপোর্ট মোছা
        db.execute("DELETE FROM resource_reports WHERE resource_id=%s", (r["resource_id"],))
        db.execute("DELETE FROM resources WHERE id=%s", (r["resource_id"],))
    else:                     # শুধু এই রিপোর্ট বাতিল
        db.execute("DELETE FROM resource_reports WHERE id=%s", (report_id,))


# =============================== (২) মেনু ===============================

def ask(prompt, default=""):
    value = input(f"{prompt}{f' [{default}]' if default else ''}: ").strip()
    return value or default


def ask_new_password(label="Password"):
    first = getpass.getpass(f"{label}: ")       # টাইপ করা অক্ষর পর্দায় দেখায় না
    if first != getpass.getpass("Confirm password: "):
        raise ValueError("Passwords do not match")
    return first


def ask_int(prompt):
    value = ask(prompt)
    return int(value) if value.isdigit() else None


def choose(title, options):
    """options = [(লেখা, ফাংশন), ...]; বাছা অপশনের ফাংশন ফেরত দেয়"""
    print(f"\n{'=' * 50}\n{title}\n{'=' * 50}")
    for n, (label, _) in enumerate(options, 1):
        print(f"  {n}) {label}")
    pick = ask("Choose")
    if pick.isdigit() and 1 <= int(pick) <= len(options):
        return options[int(pick) - 1][1]
    print("Invalid choice.")


def show_table(headers, rows):
    rows = [[str(c) for c in r] for r in rows]
    w = [max([len(h)] + [len(r[i]) for r in rows]) for i, h in enumerate(headers)]
    print("  ".join(h.ljust(w[i]) for i, h in enumerate(headers)))
    for r in rows:
        print("  ".join(c.ljust(w[i]) for i, c in enumerate(r)))
    if not rows:
        print("(empty)")


def ask_academic(now=("", "", "", "")):
    return (ask("University", now[0]), ask("Department", now[1]),
            ask("Intake", now[2]), ask("Section", now[3]))


def m_register():
    print("\n-- Create account (University etc. can be left empty) --")
    username, email, student_id = ask("Username"), ask("Email"), ask("Student ID")
    password = ask_new_password()
    register(username, email, password, student_id, *ask_academic())
    print("Account created. A 6-digit code was sent to your email.")
    m_verify(email)


def m_verify(email=None):
    email = email or ask("Email")
    code = ask("6-digit code (type r to resend)")
    if code.lower() == "r":
        resend_code(email)
        print("A new code was sent. Choose 'Verify email' again.")
        return
    verify(email, code)
    print("Account verified. You can log in now.")


def m_login():
    login(ask("Username"), getpass.getpass("Password: "))
    print(f"Welcome, {current_user['username']}!")


def m_forgot():
    email = ask("Your email")
    request_reset(email)
    print("If the email exists, a 6-digit code has been sent.")
    code = ask("Code")
    reset_password(email, code, ask_new_password("New password"))
    print("Password changed. Please log in.")


def m_profile():
    u = current_user
    names = [n or "-" for n in academic_names(u["id"])]
    print(f"\nUsername: {u['username']}   Email: {u['email']}   Role: {u['role']}")
    print(f"Full name: {u['full_name'] or '-'}   Student ID: {u['student_id'] or '-'}   Birthday: {u['birthday'] or '-'}")
    print(f"University: {names[0]}   Department: {names[1]}   Intake: {names[2]}   Section: {names[3]}")


def m_edit_profile():
    u = current_user
    print("\n-- Edit profile (press Enter to keep the current value) --")
    old_birthday = u["birthday"].strftime("%Y-%m-%d") if u["birthday"] else ""
    update_profile(ask("Full name", u["full_name"] or ""), ask("Student ID", u["student_id"] or ""),
                   ask("Birthday (YYYY-MM-DD)", old_birthday), *ask_academic(academic_names(u["id"])))
    print("Profile updated.")


def m_change_password():
    old = getpass.getpass("Old password: ")
    change_password(old, ask_new_password("New password"))
    print("Password changed.")


def m_users():
    show_table(["ID", "Username", "Email", "Role", "Active"],
               [(u["id"], u["username"], u["email"], u["role"], "yes" if u["is_active"] else "no")
                for u in admin_users()])


def m_active():
    m_users()
    user_id = ask_int("User ID")
    if user_id:
        admin_set_active(user_id, ask("a = activate, d = deactivate").lower() == "a")
        print("Done.")


def m_role():
    m_users()
    user_id = ask_int("User ID")
    if user_id:
        admin_set_role(user_id, ask("New role (student/admin)").lower())
        print("Role updated.")


def m_delete():
    m_users()
    user_id = ask_int("User ID to delete")
    if user_id and ask("Are you sure? (y/n)", "n").lower() == "y":
        admin_delete_user(user_id)
        print("User deleted.")


def m_reports():
    rows = admin_reports()
    if rows is None:
        print("The resources module is not installed yet.")
        return
    show_table(["ID", "Resource", "Reason"], [(r["id"], r["title"], r["reason"] or "-") for r in rows])
    report_id = ask_int("Report ID (Enter to go back)")
    if report_id:
        choice = ask("d = delete the resource, x = dismiss the report").lower()
        if choice in ("d", "x"):
            admin_report_action(report_id, choice == "d")
            print("Done.")


def run(action):
    """মেনুর কাজ চালায়; ভুল (ValueError) হলে বার্তা দেখায়, প্রোগ্রাম বন্ধ হয় না"""
    try:
        action()
    except ValueError as error:
        print(f"\n[!] {error}")


def admin_menu():
    while True:
        action = choose("Admin panel", [
            ("List users", m_users), ("Activate / deactivate user", m_active),
            ("Change user role", m_role), ("Delete user", m_delete),
            ("Reported content", m_reports), ("Back", "back")])
        if action == "back":
            return
        if action:
            run(action)


# =============================== (৩) মূল লুপ ===============================

def main():
    try:
        db.one("SELECT 1 AS ok")
    except Exception as error:
        print("Cannot connect to MySQL:", error)
        print("Check: MySQL is running, schema.sql was run, and local_config.py has your password.")
        sys.exit(1)

    print("Welcome to Student Assistance")
    try:
        while True:
            if current_user:        # লগইনের পরের মেনু
                options = [("My profile", m_profile), ("Edit profile", m_edit_profile),
                           ("Change password", m_change_password)]
                if current_user["role"] == "admin":
                    options.append(("Admin panel", admin_menu))
                options.append(("Logout", logout))
                action = choose(f"Dashboard ({current_user['username']})", options)
            else:                   # লগইনের আগের মেনু
                action = choose("Student Assistance", [
                    ("Login", m_login), ("Create account", m_register), ("Verify email", m_verify),
                    ("Forgot password", m_forgot), ("Exit", "exit")])
                if action == "exit":
                    break
            if action:
                run(action)
    except (KeyboardInterrupt, EOFError):
        pass
    print("\nBye!")


if __name__ == "__main__":
    main()
