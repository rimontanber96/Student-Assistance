"""Group tasks: add, assign, change status, delete."""
from .helpers import ask, line, to_int
from .members import is_member
from .models import GroupTask

STATUSES = ("todo", "doing", "done")


# ---------- logic ----------
def tasks_of(db, group_id):
    return [t for t in db.tasks if t.group_id == group_id]


def find_task(db, group_id, task_id):
    for t in db.tasks:
        if t.id == task_id and t.group_id == group_id:
            return t
    return None


def add_task(db, group_id, title, assigned_to, created_by, due_date):
    db.tasks.append(GroupTask(db.new_id(), group_id, title, assigned_to, created_by, due_date))
    db.save()


def set_task_status(db, task, status):
    task.status = status
    db.save()


def delete_task(db, task):
    db.tasks.remove(task)
    db.save()


# ---------- console ----------
def show_tasks(db, group):
    line()
    print("TASKS")
    items = tasks_of(db, group.id)
    if not items:
        print("  (none yet)")
    for t in items:
        print(f"  #{t.id} [{t.status}] {t.title}  | assigned: {t.assigned_to or '-'} | due: {t.due_date or '-'}")


def add_task_menu(db, user, group):
    title = ask("Task title: ")
    if not title:
        print("Title is required.")
        return
    assigned = ask("Assign to username (optional): ")
    if assigned and not is_member(db, group.id, assigned):
        print("That user is not in this group. Task will be unassigned.")
        assigned = ""
    due = ask("Due date YYYY-MM-DD (optional): ")
    add_task(db, group.id, title, assigned, user, due)
    print("Task added.")


def change_status_menu(db, user, group):
    show_tasks(db, group)
    tid = to_int(ask("Task id: "))
    task = find_task(db, group.id, tid) if tid is not None else None
    if not task:
        print("Task not found.")
        return
    status = ask("New status (todo / doing / done): ").lower()
    if status in STATUSES:
        set_task_status(db, task, status)
        print("Updated.")
    else:
        print("Invalid status.")


def delete_task_menu(db, user, group):
    show_tasks(db, group)
    tid = to_int(ask("Task id to delete: "))
    task = find_task(db, group.id, tid) if tid is not None else None
    if task:
        delete_task(db, task)
        print("Deleted.")
    else:
        print("Task not found.")
