import os
import sqlite3

class SQLiteConn:

    def __init__(self):
        self.conn = None
        self.cursor = None

    # open the connection to the database
    def open(self):
        self.conn = sqlite3.connect(os.path.dirname(os.path.dirname(__file__)) + "/data/todolist.db")
        self.cursor = self.conn.cursor()

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
    def add_entry(self, title, date, priority, category, description):
        query = "INSERT INTO tasks (title, date, priority, category, description) VALUES (?, ?, ?, ?, ?)"
        params = (title, date, priority.value, category, description)
        self.execute(query, params)

    # remove an entry from the database
    def remove_entry(self, taskID):
        query = "DELETE FROM tasks WHERE taskID = ?"
        params = (taskID,)
        self.execute(query, params)

    # update an entry in the database
    def update_entry(self, taskID, title=None, date=None, priority=None, category=None, description=None):
        query = "UPDATE tasks SET "
        params = []
        if title is not None:
            query += "title = ?, "
            params.append(title)
        if date is not None:
            query += "date = ?, "
            params.append(date)
        if priority is not None:
            query += "priority = ?, "
            params.append(priority.value)
        if category is not None:
            query += "category = ?, "
            params.append(category)
        if description is not None:
            query += "description = ?, "
            params.append(description)
        query = query.rstrip(", ") 
        query += " WHERE taskID = ?"
        params.append(taskID)
        self.execute(query, tuple(params))

    # fetch all entries from the database. returns a list or None
    def fetch_all_entries(self):
        query = "SELECT * FROM tasks"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # fetch an entry from the database by its ID. returns a tuple or None
    def fetch_entry_by_id(self, taskID):
        query = "SELECT * FROM tasks WHERE taskID = ?"
        self.cursor.execute(query, (taskID,))
        return self.cursor.fetchone()
    
    # toggle the completion status of an entry
    def toggle_entry_completion(self, taskID):
        query = "SELECT isComplete FROM tasks WHERE taskID = ?"
        self.cursor.execute(query, (taskID,))
        result = self.cursor.fetchone()
        if result:
            isComplete = not result[0]
            query = "UPDATE tasks SET isComplete = ? WHERE taskID = ?"
            self.execute(query, (isComplete, taskID))
        else:
            print(f"No entry found with taskID: {taskID}")