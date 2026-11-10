"""Share study materials (file path or link) inside a group."""
from .helpers import ask, line, to_int
from .members import is_admin
from .models import StudyMaterial


# ---------- logic ----------
def materials_of(db, group_id):
    return [m for m in db.materials if m.group_id == group_id]


def find_material(db, group_id, material_id):
    for m in db.materials:
        if m.id == material_id and m.group_id == group_id:
            return m
    return None


def share_material(db, group_id, title, location, uploaded_by):
    db.materials.append(StudyMaterial(db.new_id(), group_id, title, location, uploaded_by))
    db.save()


def delete_material(db, material):
    db.materials.remove(material)
    db.save()


# ---------- console ----------
def show_materials(db, group):
    line()
    print("MATERIALS")
    items = materials_of(db, group.id)
    if not items:
        print("  (none yet)")
    for m in items:
        print(f"  #{m.id} {m.title}  ->  {m.location}   [by {m.uploaded_by}]")


def share_material_menu(db, user, group):
    title = ask("Title: ")
    location = ask("File path or link: ")
    if title and location:
        share_material(db, group.id, title, location, user)
        print("Material shared.")
    else:
        print("Title and location are required.")


def delete_material_menu(db, user, group):
    show_materials(db, group)
    mid = to_int(ask("Material id to delete: "))
    material = find_material(db, group.id, mid) if mid is not None else None
    if not material:
        print("Material not found.")
    elif material.uploaded_by != user and not is_admin(db, group.id, user):
        print("Only the uploader or an admin can delete this.")
    else:
        delete_material(db, material)
        print("Deleted.")
