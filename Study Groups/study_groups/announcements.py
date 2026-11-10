"""Group announcements (only admins can post)."""
from .helpers import ask, line
from .members import is_admin
from .models import GroupAnnouncement


# ---------- logic ----------
def announcements_of(db, group_id):
    """Newest first."""
    return [a for a in db.announcements if a.group_id == group_id][::-1]


def post_announcement(db, group_id, author, message):
    db.announcements.append(GroupAnnouncement(db.new_id(), group_id, author, message))
    db.save()


# ---------- console ----------
def show_announcements(db, group):
    line()
    print("ANNOUNCEMENTS")
    items = announcements_of(db, group.id)
    if not items:
        print("  (none yet)")
    for a in items:
        print(f"  {a.author}: {a.message}")


def post_announcement_menu(db, user, group):
    if not is_admin(db, group.id, user):
        print("Only admins can post announcements.")
        return
    msg = ask("Message: ")
    if msg:
        post_announcement(db, group.id, user, msg)
        print("Posted.")
