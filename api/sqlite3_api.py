import data.task as task
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

        # Create the tasks table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                taskID INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                date TEXT NOT NULL,
                                priority INTEGER NOT NULL,
                                category TEXT NOT NULL,
                                description TEXT NOT NULL,
                                isComplete BOOLEAN NOT NULL CHECK (isComplete IN (0, 1))
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
    def add_entry(self, title, date, priority, category, description, completion=False):
        query = "INSERT INTO tasks (title, date, priority, category, description, isComplete) VALUES (?, ?, ?, ?, ?, ?)"
        params = (title, date, priority.value, category, description, int(completion))
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
    def update_entry(self, taskID, title=None, date=None, priority=None, category=None, description=None, completion=None):
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
        if completion is not None:
            query += "isComplete = ?, "
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
            converted = []
            converted.append(int(row[0]))   # Convert taskID to int
            converted.append(row[1])        # Keep title as is
            converted.append(row[2])        # Keep date as is
            converted.append(int(row[3]))   # Convert priority to int
            converted.append(row[4])        # Keep category as is
            converted.append(row[5])        # Keep description as is
            converted.append(bool(row[6]))  # Convert isComplete to bool

            newTask = task.Task(converted[1], converted[2], converted[3], converted[4], converted[5], converted[6])

            # Set the taskID for the Task object
            newTask.taskID = converted[0]  

            results.append(newTask)

        return results if results else None

    # fetch an entry from the database by its ID. returns a Task object or None
    def fetch_entry_by_id(self, taskID):
        query = "SELECT * FROM tasks WHERE taskID = ?"
        self.cursor.execute(query, (taskID,))

        result = self.cursor.fetchone()
        if result:
            result = list(result)
            result[0] = int(result[0])      # Convert taskID to int
            result[3] = int(result[3])      # Convert priority to int
            result[6] = bool(result[6])     # Convert isComplete to bool

            newTask = task.Task(result[1], result[2], result[3], result[4], result[5], result[6])
            newTask.taskID = result[0]  # Set the taskID for the Task object

            return newTask
        else:
            return None
    
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