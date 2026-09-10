import os
import sqlite3

from data import task


class SQLiteConn:

    def __init__(self):
        self.conn = None
        self.cursor = None

    # open the connection to the database
    def open(self):
        self.conn = sqlite3.connect(os.path.dirname(os.path.dirname(__file__)) + "/data/todolist.db")
        self.cursor = self.conn.cursor()

        # Create the tasks table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                taskID INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                dateAdded TEXT NOT NULL,
                                dateDue TEXT NOT NULL,
                                priority INTEGER NOT NULL,
                                category TEXT NOT NULL,
                                details TEXT NOT NULL,
                                is_complete BOOLEAN NOT NULL CHECK (is_complete IN (0, 1))
                            )''')
        self.conn.commit()

    # close the connection to the database
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    # execute the query 
    def execute(self, query, params=None):
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        self.conn.commit()

    # add an entry to the database
    def add_entry(self, title, dateAdded, dateDue, priority, category, details, completion=False):
        query = "INSERT INTO tasks (title, dateAdded, dateDue, priority, category, details, is_complete) VALUES (?, ?, ?, ?, ?, ?, ?)"
        priority_value = getattr(priority, "value", priority)
        params = (title, dateAdded, dateDue, priority_value, category, details, int(completion))
        self.execute(query, params)

        # return the id to assign to Task object based on database increments
        query = "SELECT last_insert_rowid()"
        self.cursor.execute(query)
        last_id = self.cursor.fetchone()[0]
        return last_id

    # remove an entry from the database
    def remove_entry(self, taskID):
        query = "DELETE FROM tasks WHERE taskID = ?"
        params = (taskID,)
        self.execute(query, params)

    # update an entry in the database
    def update_entry(self, taskID, title=None, dateAdded=None, dateDue=None, priority=None, category=None, details=None, completion=None):
        query = "UPDATE tasks SET "
        params = []
        if title is not None:
            query += "title = ?, "
            params.append(title)
        if dateAdded is not None:
            query += "dateAdded = ?, "
            params.append(dateAdded)
        if dateDue is not None:
            query += "dateDue = ?, "
            params.append(dateDue)
        if priority is not None:
            query += "priority = ?, "
            params.append(getattr(priority, "value", priority))
        if category is not None:
            query += "category = ?, "
            params.append(category)
        if details is not None:
            query += "details = ?, "
            params.append(details)
        if completion is not None:
            query += "is_complete = ?, "
            params.append(int(completion))
        query = query.rstrip(", ") 
        query += " WHERE taskID = ?"
        params.append(taskID)
        self.execute(query, tuple(params))

    # fetch all entries from the database. returns a list or None
    def fetch_all_entries(self):
        query = "SELECT * FROM tasks"
        self.cursor.execute(query)

        results = []

        for row in self.cursor.fetchall():
            new_task = task.Task(
                row[1],  # title
                row[2],  # dateAdded
                row[3],  # dateDue
                row[4],  # priority
                row[5],  # category
                row[6],  # details
                bool(row[7])  # is_complete
            )
            new_task.taskID = int(row[0])
            results.append(new_task)

        return results if results else None

    # fetch an entry from the database by its ID. returns a Task object or None
    def fetch_entry_by_id(self, taskID):
        query = "SELECT * FROM tasks WHERE taskID = ?"
        self.cursor.execute(query, (taskID,))

        result = self.cursor.fetchone()
        if result:
            new_task = task.Task(
                result[1],  # title
                result[2],  # dateAdded
                result[3],  # dateDue
                int(result[4]),  # priority
                result[5],  # category
                result[6],  # details
                bool(result[7])  # is_complete
            )
            new_task.taskID = int(result[0])
            return new_task

        return None
    
    # toggle the completion status of an entry
    def toggle_entry_completion(self, taskID):
        query = "SELECT is_complete FROM tasks WHERE taskID = ?"
        self.cursor.execute(query, (taskID,))
        result = self.cursor.fetchone()
        if result:
            is_complete = not result[0]
            query = "UPDATE tasks SET is_complete = ? WHERE taskID = ?"
            self.execute(query, (is_complete, taskID))
        else:
            print(f"No entry found with taskID: {taskID}")