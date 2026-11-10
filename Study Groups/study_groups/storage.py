"""Keeps all data in memory and saves/loads it to one JSON text file."""
import json

from .models import (GroupAnnouncement, GroupMember, GroupTask,
                     StudyGroup, StudyMaterial)

DATA_FILE = "study_groups_data.json"


class Storage:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.users = []
        self.groups = []
        self.members = []
        self.tasks = []
        self.materials = []
        self.announcements = []
        self.next_id = 1
        self.load()

    def new_id(self):
        n = self.next_id
        self.next_id += 1
        return n

    def register_user(self, username):
        if username not in self.users:
            self.users.append(username)
            self.save()

    def save(self):
        data = {
            "next_id": self.next_id,
            "users": self.users,
            "groups": [g.__dict__ for g in self.groups],
            "members": [m.__dict__ for m in self.members],
            "tasks": [t.__dict__ for t in self.tasks],
            "materials": [m.__dict__ for m in self.materials],
            "announcements": [a.__dict__ for a in self.announcements],
        }
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        try:
            with open(self.filename) as f:
                data = json.load(f)
        except (FileNotFoundError, ValueError):
            return
        self.next_id = data.get("next_id", 1)
        self.users = data.get("users", [])
        self.groups = [StudyGroup(**d) for d in data.get("groups", [])]
        self.members = [GroupMember(**d) for d in data.get("members", [])]
        self.tasks = [GroupTask(**d) for d in data.get("tasks", [])]
        self.materials = [StudyMaterial(**d) for d in data.get("materials", [])]
        self.announcements = [GroupAnnouncement(**d) for d in data.get("announcements", [])]
