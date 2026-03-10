import tkinter as tk
from tkinter import messagebox

# =========================
# User Class
# =========================
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.approved = False

    def request_access(self):
        if self.email.endswith("@albright.edu"):
            self.approved = True
            return True
        return False


# =========================
# Event Class
# =========================
class Event:
    def __init__(self, title, date, time, category, description):
        self.title = title
        self.date = date
        self.time = time
        self.category = category
        self.description = description

    def display(self):
        return f"{self.date} | {self.time} | {self.title} ({self.category})"


# =========================
# Calendar Class
# =========================
class Calendar:
    def __init__(self):
        self.events = []
        self.authorized_users = []

    def add_user(self, user):
        if user.approved:
