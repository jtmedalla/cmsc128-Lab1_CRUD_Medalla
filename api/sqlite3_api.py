import hashlib
import hmac
import os
import secrets
import sqlite3
import time

import bcrypt
import keyring

from data import task

KEYRING_SERVICE = "python-todolist"
KEYRING_ACCOUNT = "current-session"


def get_pw_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class SQLiteConn:

    def __init__(self):
        self.conn = None
        self.cursor = None

    # open the connection to the database
    def open(self):
        self.conn = sqlite3.connect(os.path.dirname(os.path.dirname(__file__)) + "/data/todolist.db")
        self.cursor = self.conn.cursor()

        # create the users table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                userID INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL
                            )''')

        # Create the tasks table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                taskID INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                dateAdded TEXT NOT NULL,
                                dateDue TEXT NOT NULL,
                                priority INTEGER NOT NULL,
                                category TEXT NOT NULL,
                                details TEXT NOT NULL,
                                is_complete BOOLEAN NOT NULL CHECK (is_complete IN (0, 1)),
                                user_id INTEGER NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES users(userID)
                            )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                                sessionID INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                token_hash TEXT NOT NULL UNIQUE,
                                expires_at INTEGER NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES users(userID)
                            )''')
        
        
        self.conn.commit()

    # close the connection to the database
    def close(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None

    # execute the query 
    def execute(self, query, params=None):
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        self.conn.commit()

    # add an entry to the database
    def add_entry(self, title, dateAdded, dateDue, priority, category, details, completion=False, user_id=None):
        query = "INSERT INTO tasks (title, dateAdded, dateDue, priority, category, details, is_complete, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        priority_value = getattr(priority, "value", priority)
        params = (title, dateAdded, dateDue, priority_value, category, details, int(completion), user_id)
        self.execute(query, params)

        # return the id to assign to Task object based on database increments
        query = "SELECT last_insert_rowid()"
        self.cursor.execute(query)
        last_id = self.cursor.fetchone()[0]
        return last_id

    # remove an entry from the database
    def remove_entry(self, taskID, user_id):
        query = "DELETE FROM tasks WHERE taskID = ? AND user_id = ?"
        params = (taskID, user_id)
        self.execute(query, params)

    # update an entry in the database
    def update_entry(self, taskID, title=None, dateAdded=None, dateDue=None, priority=None, category=None, details=None, completion=None, user_id=None):
        if user_id is None:
            raise ValueError("user_id must be provided to update an entry.")

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
        query += " WHERE taskID = ? AND user_id = ?"
        params.append(taskID)
        params.append(user_id)
        self.execute(query, tuple(params))

    # fetch all entries from the database. returns a list or None
    def fetch_all_entries(self, user_id):
        query = "SELECT * FROM tasks WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))

        results = []

        for row in self.cursor.fetchall():
            new_task = task.Task(
                row[1],  # title
                row[2],  # dateAdded
                row[3],  # dateDue
                row[4],  # priority
                row[5],  # category
                row[6],  # details
                bool(row[7]),  # is_complete
                row[8]  # user_id
            )
            new_task.taskID = int(row[0])
            results.append(new_task)

        return results if results else None

    # fetch an entry from the database by its ID. returns a Task object or None
    def fetch_entry_by_id(self, taskID, user_id):
        query = "SELECT * FROM tasks WHERE taskID = ? AND user_id = ?"
        self.cursor.execute(query, (taskID, user_id))

        result = self.cursor.fetchone()
        if result:
            new_task = task.Task(
                result[1],  # title
                result[2],  # dateAdded
                result[3],  # dateDue
                int(result[4]),  # priority
                result[5],  # category
                result[6],  # details
                bool(result[7]),  # is_complete
                result[8]  # user_id
            )
            new_task.taskID = int(result[0])
            return new_task

        return None
    
    # toggle the completion status of an entry
    def toggle_entry_completion(self, taskID, user_id):
        query = "SELECT is_complete FROM tasks WHERE taskID = ? AND user_id = ?"
        self.cursor.execute(query, (taskID, user_id))
        result = self.cursor.fetchone()
        if result:
            is_complete = not result[0]
            query = "UPDATE tasks SET is_complete = ? WHERE taskID = ? AND user_id = ?"
            self.execute(query, (is_complete, taskID, user_id))
        else:
            print(f"No entry found with taskID: {taskID}")

    def add_user(self, username, password):
        query = "SELECT * FROM users WHERE username = ?"
        params = (username,)
        self.cursor.execute(query, params)
        result = self.cursor.fetchone()
        if result:
            return False  # User already exists

        hashed_pw = get_pw_hash(password)

        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        params = (username, hashed_pw)
        self.execute(query, params)
        return True

    def get_username_by_id(self, user_id):
        query = "SELECT username FROM users WHERE userID = ?"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def authenticate_user(self, username, password):
        self.cursor.execute(
            "SELECT userID, password FROM users WHERE username = ?",
            (username,)
        )

        result = self.cursor.fetchone()

        if result and bcrypt.checkpw(
            password.encode("utf-8"),
            result[1]
        ):
            return result[0]  # userID

        return None

    
    def create_session(self, user_id):
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        expires_at = int(time.time()) + (30 * 24 * 60 * 60)

        # Delete any existing sessions for the user before creating a new one
        self.execute(
            "DELETE FROM sessions"
        )

        # delete keyring credentials if it exists to avoid duplicates
        try:
            keyring.delete_password(KEYRING_SERVICE, KEYRING_ACCOUNT)
        except keyring.errors.PasswordDeleteError:
            pass

        self.execute(
            "INSERT INTO sessions (user_id, token_hash, expires_at) VALUES (?, ?, ?)",
            (user_id, token_hash, expires_at)
        )

        # Store the token using the operating system's secure credential store.
        keyring.set_password(KEYRING_SERVICE, KEYRING_ACCOUNT, token)

        return token

    def compare_token(self, candidate_token):
        #  Return the user ID if the candidate token is valid.
        if not candidate_token:
            return None

        candidate_hash = hashlib.sha256(
            candidate_token.encode("utf-8")
        ).hexdigest()

        self.cursor.execute(
            """SELECT user_id, token_hash
               FROM sessions
               WHERE expires_at > ?""",
            (int(time.time()),)
        )

        for user_id, stored_hash in self.cursor.fetchall():
            if hmac.compare_digest(candidate_hash, stored_hash):
                return user_id

        return None

    def restore_session(self):
        token = keyring.get_password(
            KEYRING_SERVICE,
            KEYRING_ACCOUNT
        )

        user_id = self.compare_token(token)

        if user_id is None and token:
            try:
                keyring.delete_password(
                    KEYRING_SERVICE,
                    KEYRING_ACCOUNT
                )
            except keyring.errors.PasswordDeleteError:
                pass

        return user_id

    def logout(self):
        token = keyring.get_password(KEYRING_SERVICE, KEYRING_ACCOUNT)

        if token:
            token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
            self.execute(
                "DELETE FROM sessions WHERE token_hash = ?",
                (token_hash,)
            )

            try:
                keyring.delete_password(KEYRING_SERVICE, KEYRING_ACCOUNT)
            except keyring.errors.PasswordDeleteError:
                pass