from db import create_tables

from auth import register, login

from services.task_service import (
    add_task, view_tasks, complete_task
)

from services.timetable_service import (
    add_timetable, view_timetable
)

from services.notes_service import (
    add_note, view_notes
)

from services.progress_service import (
    add_progress, view_progress
)


def main():

    create_tables()

    while True:

        print("\n===== STUDY PLANNER =====")

        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            register()

        elif choice == "2":

            user_id = login()

            if user_id:
                dashboard(user_id)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


def dashboard(user_id):

    while True:

        print("\n===== STUDENT DASHBOARD =====")

        print("1. Personal Tasks")
        print("2. Class Timetable")
        print("3. Study Notes")
        print("4. Study Progress")
        print("5. Logout")

        choice = input("Choose option: ")

        if choice == "1":

            print("\n1. Add Task")
            print("2. View Tasks")
            print("3. Complete Task")

            option = input("Choose: ")

            if option == "1":
                add_task(user_id)

            elif option == "2":
                view_tasks(user_id)

            elif option == "3":
                complete_task(user_id)

        elif choice == "2":

            print("\n1. Add Timetable")
            print("2. View Timetable")

            option = input("Choose: ")

            if option == "1":
                add_timetable(user_id)

            elif option == "2":
                view_timetable(user_id)

        elif choice == "3":

            print("\n1. Add Note")
            print("2. View Notes")

            option = input("Choose: ")

            if option == "1":
                add_note(user_id)

            elif option == "2":
                view_notes(user_id)

        elif choice == "4":

            print("\n1. Add Progress")
            print("2. View Progress")

            option = input("Choose: ")

            if option == "1":
                add_progress(user_id)

            elif option == "2":
                view_progress(user_id)

        elif choice == "5":
            print("Logged out!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()