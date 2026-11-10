"""Create study groups, join with a code, list and delete groups."""
from .helpers import ask, line, to_int
from .members import is_member
from .models import GroupMember, StudyGroup


# ---------- logic ----------
def get_group(db, group_id):
    for g in db.groups:
        if g.id == group_id:
            return g
    return None


def create_group(db, name, course, description, owner):
    gid = db.new_id()
    code = "SG" + str(1000 + gid)
    db.groups.append(StudyGroup(gid, name, course, description, owner, code))
    db.members.append(GroupMember(gid, owner, "admin"))  # creator is admin
    db.save()
    return get_group(db, gid)


def join_group(db, username, code):
    """Returns (group, already_member). group is None if the code is wrong."""
    for g in db.groups:
        if g.join_code == code.strip().upper():
            if is_member(db, g.id, username):
                return g, True
            db.members.append(GroupMember(g.id, username))
            db.save()
            return g, False
    return None, False


def groups_for(db, username):
    return [g for g in db.groups if is_member(db, g.id, username)]


def delete_group(db, group_id):
    db.groups = [g for g in db.groups if g.id != group_id]
    db.members = [m for m in db.members if m.group_id != group_id]
    db.tasks = [t for t in db.tasks if t.group_id != group_id]
    db.materials = [m for m in db.materials if m.group_id != group_id]
    db.announcements = [a for a in db.announcements if a.group_id != group_id]
    db.save()


# ---------- console ----------
def list_my_groups_menu(db, user):
    groups = groups_for(db, user)
    if not groups:
        print("You are not in any group yet.")
    for g in groups:
        print(f"  #{g.id} {g.name}  | course: {g.course or '-'}  | code: {g.join_code}")


def create_group_menu(db, user):
    name = ask("Group name: ")
    if not name:
        print("Name is required.")
        return
    course = ask("Course (optional): ")
    desc = ask("Description (optional): ")
    g = create_group(db, name, course, desc, user)
    print(f"Group created! Share this join code: {g.join_code}")


def join_group_menu(db, user):
    code = ask("Join code: ")
    g, already = join_group(db, user, code)
    if not g:
        print("Invalid join code.")
    elif already:
        print("You are already a member of", g.name)
    else:
        print("Joined", g.name)


def pick_group_menu(db, user):
    """Ask for a group id; return the group if the user is a member, else None."""
    gid = to_int(ask("Group id: "))
    g = get_group(db, gid) if gid is not None else None
    if g and is_member(db, g.id, user):
        return g
    print("Group not found, or you are not a member.")
    return None


def delete_group_menu(db, user, group):
    """Returns True if the group was deleted."""
    if group.owner != user:
        print("Only the owner can delete the group.")
        return False
    if ask(f"Delete '{group.name}' and everything in it? (yes/no): ").lower() == "yes":
        delete_group(db, group.id)
        print("Group deleted.")
        return True
    return False
