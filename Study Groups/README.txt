STUDY GROUPS - Student Assistance System
========================================
Pure Python console app (no tkinter, no sqlite3, no framework).
Data is saved in study_groups_data.json (built-in json module only).

Folder structure
----------------
main.py                          -> run this file (all menus)
study_groups/
    models.py                    -> StudyGroup, GroupMember, GroupTask,
                                    StudyMaterial, GroupAnnouncement
    storage.py                   -> keeps data + save/load JSON file
    helpers.py                   -> ask(), line(), to_int()
    create_join_group.py         -> create group, join with code, list, delete
    members.py                   -> view, add, remove/leave members, admin check
    materials.py                 -> share study materials (file path / link)
    tasks.py                     -> group tasks (assign, due date, status)
    announcements.py             -> group announcements (admin only)

How to run
----------
    cd study_groups_project
    python main.py

Note: a user must log in once before an admin can add them.
