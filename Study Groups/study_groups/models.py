"""Models: StudyGroup, GroupMember, GroupTask, StudyMaterial, GroupAnnouncement."""


class StudyGroup:
    def __init__(self, id, name, course, description, owner, join_code):
        self.id = id
        self.name = name
        self.course = course
        self.description = description
        self.owner = owner
        self.join_code = join_code


class GroupMember:
    def __init__(self, group_id, username, role="member"):
        self.group_id = group_id
        self.username = username
        self.role = role  # "admin" or "member"


class GroupTask:
    def __init__(self, id, group_id, title, assigned_to, created_by, due_date, status="todo"):
        self.id = id
        self.group_id = group_id
        self.title = title
        self.assigned_to = assigned_to
        self.created_by = created_by
        self.due_date = due_date
        self.status = status  # todo / doing / done


class StudyMaterial:
    def __init__(self, id, group_id, title, location, uploaded_by):
        self.id = id
        self.group_id = group_id
        self.title = title
        self.location = location  # file path or link
        self.uploaded_by = uploaded_by


class GroupAnnouncement:
    def __init__(self, id, group_id, author, message):
        self.id = id
        self.group_id = group_id
        self.author = author
        self.message = message
