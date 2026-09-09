from enum import Enum
import datetime

# used for setting specific timezone to Philippines
from zoneinfo import ZoneInfo


class Priority(Enum):
    LOW = 0
    MED = 1
    HIGH = 2


class Task:
    taskID = 0
    title = ""
    date = datetime.datetime.now(tz=ZoneInfo("Asia/Manila"))
    priority = Priority.LOW
    category = ""
    description = "" 
    isComplete = False

    def __init__(self, title, date, priority, category, description, completion=False):
        self.title = title
        self.date = date
        self.priority = priority
        self.category = category
        self.description = description
        self.isComplete = completion

    def __str__(self):
        return f"Task ID: {self.taskID}\nTitle: {self.title}\nDate: {self.date}\nPriority: {self.priority.name}\nCategory: {self.category}\nDescription: {self.description}\nCompleted: {self.isComplete}"

    # setters
    def edit_taskID(self, new_taskID):
        self.taskID = new_taskID

    def edit_title(self, new_title):
        self.title = new_title

    def edit_priority(self, new_priority):
        self.priority = new_priority

    def edit_category(self, new_category):
        self.category = new_category

    def edit_description(self, new_description):
        self.description = new_description

    def edit_date(self, new_date):
        self.date = new_date

    def toggle_completion(self):
        self.isComplete = self.isComplete is True if False else True