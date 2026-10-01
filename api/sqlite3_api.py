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
SECURITY_QUESTIONS = (
    "What was the name of your first pet?",
    "What is your favorite color?",
    "What city were you born in?",
    "What was the name of your elementary school?",
)


def get_pw_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def hash_answer(answer):
    return bcrypt.hashpw(
        answer.strip().lower().encode("utf-8"),
        bcrypt.gensalt()
    )


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
                                password TEXT NOT NULL,
                                security_question_1 TEXT,
                                security_answer_1 BLOB,
                                security_question_2 TEXT,
                                security_answer_2 BLOB
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
        
        
        columns = {
            "security_question_1": "TEXT",
            "security_answer_1": "BLOB",
            "security_question_2": "TEXT",
            "security_answer_2": "BLOB",
        }

        existing_columns = {
            row[1]
            for row in self.cursor.execute("PRAGMA table_info(users)")
        }

        for column, data_type in columns.items():
            if column not in existing_columns:
                self.cursor.execute(
                    f"ALTER TABLE users ADD COLUMN {column} {data_type}"
                )

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



    def update_user_info(self, user_id, new_username=None, new_password=None):
        self.open()

        if new_username is None and new_password is None:
            self.close()
            return False  # Nothing to update

        if new_username:
            query = "UPDATE users SET username = ? WHERE userID = ?"
            params = (new_username, user_id)
            self.execute(query, params)

        if new_password:
            hashed_pw = get_pw_hash(new_password)
            query = "UPDATE users SET password = ? WHERE userID = ?"
            params = (hashed_pw, user_id)
            self.execute(query, params)

        self.close()

        return True

    def get_username_by_id(self, user_id):
        query = "SELECT username FROM users WHERE userID = ?"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def authenticate_user(self, username, password):
        self.open()
        self.cursor.execute(
            "SELECT userID, password FROM users WHERE username = ?",
            (username,)
        )

        result = self.cursor.fetchone()

        self.close()

        if result and bcrypt.checkpw(
            password.encode("utf-8"),
            result[1]
        ):
            return result[0]  # userID

        return None

    
    def create_session(self, user_id):
        self.open()
        
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

        self.close()

        return token

    def compare_token(self, candidate_token):
        self.open()

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

        self.close()

        return None

    def restore_session(self):
        self.open()

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

        self.close()

        return user_id

    def logout(self):
        self.open()

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

        self.close()

    def username_exists(self, username, exclude_user_id=None):
        self.open()

        query = "SELECT 1 FROM users WHERE username = ?"
        params = [username]

        if exclude_user_id is not None:
            query += " AND userID != ?"
            params.append(exclude_user_id)

        self.cursor.execute(query, params)

        return_val = self.cursor.fetchone() is not None

        self.close()

        return return_val

    def add_user(
        self,
        username,
        password,
        question_1,
        answer_1,
        question_2,
        answer_2
    ):
        self.open()

        try:
            self.cursor.execute(
                """
                INSERT INTO users (
                    username,
                    password,
                    security_question_1,
                    security_answer_1,
                    security_question_2,
                    security_answer_2
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    username,
                    get_pw_hash(password),
                    question_1,
                    hash_answer(answer_1),
                    question_2,
                    hash_answer(answer_2),
                )
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            self.close()

    def get_security_questions(self, username):
        self.open()

        self.cursor.execute(
            """
            SELECT security_question_1, security_question_2
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        result = self.cursor.fetchone()
        self.close()

        return result

    def reset_password(
        self,
        username,
        answer_1,
        answer_2,
        new_password
    ):
        self.open()

        self.cursor.execute(
            """
            SELECT security_answer_1, security_answer_2
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        result = self.cursor.fetchone()

        if result is None or result[0] is None or result[1] is None:
            self.close()
            return False

        valid_answers = (
            bcrypt.checkpw(
                answer_1.strip().lower().encode("utf-8"),
                result[0]
            )
            and bcrypt.checkpw(
                answer_2.strip().lower().encode("utf-8"),
                result[1]
            )
        )

        if not valid_answers:
            self.close()
            return False

        self.cursor.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (get_pw_hash(new_password), username)
        )
        self.conn.commit()
        self.close()

        return True