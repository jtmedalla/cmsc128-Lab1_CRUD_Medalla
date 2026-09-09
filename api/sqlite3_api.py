import sqlite3

class SQLiteConn:

    def __init__(self):
        self.conn = None
        self.cursor = None

    # open the connection to the database
    def open(self):
        self.conn = sqlite3.connect('todoList.db')
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

    # call to add an entry to the database
    def add_entry(self, title, date, priority, category, description):
        query = "INSERT INTO tasks (title, date, priority, category, description) VALUES (?, ?, ?, ?, ?)"
        params = (title, date, priority.value, category, description)
        self.execute(query, params)