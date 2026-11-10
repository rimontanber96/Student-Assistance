"""
Student Assistance System - Study Groups module (console app)
Pure Python: no tkinter, no sqlite3, no framework.

Run:  python main.py
"""
from study_groups import (announcements, create_join_group, materials,
                          members, tasks)
from study_groups.helpers import ask, line
from study_groups.storage import Storage


def group_menu(db, user, group):
    while True:
        line()
        print(f"GROUP: {group.name}  | Course: {group.course or '-'}  | Join code: {group.join_code}")
        print("MEMBERS        1. View   2. Add (admin)   3. Remove / leave")
        print("MATERIALS      4. View   5. Share         6. Delete")
        print("TASKS          7. View   8. Add   9. Change status   10. Delete")
        print("ANNOUNCEMENTS  11. View  12. Post (admin)")
        print("GROUP          13. Delete group (owner)")
        print("0. Back")
        choice = ask("Choose: ")

        if choice == "1":
            members.show_members(db, group)
        elif choice == "2":
            members.add_member_menu(db, user, group)
        elif choice == "3":
            if members.remove_member_menu(db, user, group):
                return  # user left the group
        elif choice == "4":
            materials.show_materials(db, group)
        elif choice == "5":
            materials.share_material_menu(db, user, group)
        elif choice == "6":
            materials.delete_material_menu(db, user, group)
        elif choice == "7":
            tasks.show_tasks(db, group)
        elif choice == "8":
            tasks.add_task_menu(db, user, group)
        elif choice == "9":
            tasks.change_status_menu(db, user, group)
        elif choice == "10":
            tasks.delete_task_menu(db, user, group)
        elif choice == "11":
            announcements.show_announcements(db, group)
        elif choice == "12":
            announcements.post_announcement_menu(db, user, group)
        elif choice == "13":
            if create_join_group.delete_group_menu(db, user, group):
                return
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def main():
    db = Storage()
    print("=== Student Assistance System: Study Groups ===")
    user = ask("Enter your username: ")
    if not user:
        print("Username is required.")
        return
    db.register_user(user)

    while True:
        line()
        print(f"MAIN MENU  (logged in as {user})")
        print("1. My groups")
        print("2. Create group")
        print("3. Join group with code")
        print("4. Open a group")
        print("0. Exit")
        choice = ask("Choose: ")

        if choice == "1":
            create_join_group.list_my_groups_menu(db, user)
        elif choice == "2":
            create_join_group.create_group_menu(db, user)
        elif choice == "3":
            create_join_group.join_group_menu(db, user)
        elif choice == "4":
            group = create_join_group.pick_group_menu(db, user)
            if group:
                group_menu(db, user, group)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
