"""Group members: view, add, remove / leave, and permission checks."""
from .helpers import ask, line
from .models import GroupMember


# ---------- logic ----------
def members_of(db, group_id):
    return [m for m in db.members if m.group_id == group_id]


def is_member(db, group_id, username):
    return any(m.group_id == group_id and m.username == username for m in db.members)


def is_admin(db, group_id, username):
    return any(
        m.group_id == group_id and m.username == username and m.role == "admin"
        for m in db.members
    )


def add_member(db, group_id, username):
    """Returns 'ok', 'no_user' or 'exists'."""
    if username not in db.users:
        return "no_user"
    if is_member(db, group_id, username):
        return "exists"
    db.members.append(GroupMember(group_id, username))
    db.save()
    return "ok"


def remove_member(db, group_id, username):
    db.members = [
        m for m in db.members if not (m.group_id == group_id and m.username == username)
    ]
    db.save()


# ---------- console ----------
def show_members(db, group):
    line()
    print("MEMBERS of", group.name)
    for m in members_of(db, group.id):
        tag = " (owner)" if m.username == group.owner else ""
        print(f"  {m.username:<15} {m.role}{tag}")


def add_member_menu(db, user, group):
    if not is_admin(db, group.id, user):
        print("Only admins can add members.")
        return
    name = ask("Username to add: ")
    result = add_member(db, group.id, name)
    if result == "ok":
        print(name, "added.")
    elif result == "exists":
        print("Already a member.")
    else:
        print("No such user. The person must log in to the app once first.")


def remove_member_menu(db, user, group):
    """Returns True if the current user left the group."""
    show_members(db, group)
    name = ask("Username to remove (your own name = leave): ")
    if not is_member(db, group.id, name):
        print("That user is not in this group.")
    elif name == group.owner:
        print("The owner cannot be removed. Delete the group instead.")
    elif name != user and not is_admin(db, group.id, user):
        print("Only admins can remove other members.")
    else:
        remove_member(db, group.id, name)
        print("Done.")
        return name == user
    return False
