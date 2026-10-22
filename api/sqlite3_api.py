import hashlib
import hmac
import os
import secrets
import sqlite3
import time
from contextlib import contextmanager

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
SESSION_DURATION = 30 * 24 * 60 * 60  # 30 days in seconds


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

    @contextmanager
    def connection(self):
        self.open()
        try:
            yield self
        finally:
            self.close()

    def _add_entry_open(
        self,
        title,
        dateAdded,
        dateDue,
        priority,
        category,
        details,
        completion=False,
        user_id=None,
    ):
        query = """
            INSERT INTO tasks
            (title, dateAdded, dateDue, priority, category, details,
             is_complete, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            title,
            dateAdded,
            dateDue,
            getattr(priority, "value", priority),
            category,
            details,
            int(completion),
            user_id,
        )
        self.execute(query, params)
        return self.cursor.lastrowid

    def add_entry(
        self,
        title,
        dateAdded,
        dateDue,
        priority,
        category,
        details,
        completion=False,
        user_id=None,
    ):
        with self.connection():
            return self._add_entry_open(
                title,
                dateAdded,
                dateDue,
                priority,
                category,
                details,
                completion,
                user_id,
            )

    def add_task(
        self,
        title,
        date_added,
        date_due,
        priority,
        category,
        details,
        user_id,
        completion=False,
    ):
        if user_id is None:
            raise ValueError("user_id must be provided.")

        with self.connection():
            return self._add_entry_open(
                title,
                date_added,
                date_due,
                priority,
                category,
                details,
                completion,
                user_id,
            )

    # remove an entry from the database
    def remove_entry(self, taskID, user_id):
        with self.connection():
            self.execute(
                "DELETE FROM tasks WHERE taskID = ? AND user_id = ?",
                (taskID, user_id),
            )

    # update an entry in the database
    def update_entry(
        self,
        taskID,
        title=None,
        dateAdded=None,
        dateDue=None,
        priority=None,
        category=None,
        details=None,
        completion=None,
        user_id=None,
    ):
        if user_id is None:
            raise ValueError("user_id must be provided.")

        fields = []
        params = []

        values = {
            "title": title,
            "dateAdded": dateAdded,
            "dateDue": dateDue,
            "priority": (
                getattr(priority, "value", priority)
                if priority is not None
                else None
            ),
            "category": category,
            "details": details,
            "is_complete": (
                int(completion) if completion is not None else None
            ),
        }

        for field, value in values.items():
            if value is not None:
                fields.append(f"{field} = ?")
                params.append(value)

        if not fields:
            return

        params.extend((taskID, user_id))

        with self.connection():
            self.execute(
                f"""
                UPDATE tasks
                SET {", ".join(fields)}
                WHERE taskID = ? AND user_id = ?
                """,
                tuple(params),
            )

    # fetch all entries from the database. returns a list or None
    def fetch_all_entries(self, user_id):
        with self.connection():
            self.cursor.execute(
                "SELECT * FROM tasks WHERE user_id = ?",
                (user_id,),
            )
            rows = self.cursor.fetchall()

        results = []
        for row in rows:
            current_task = task.Task(
                row[1], row[2], row[3], row[4],
                row[5], row[6], bool(row[7]), row[8],
            )
            current_task.taskID = int(row[0])
            results.append(current_task)

        return results or None

    # fetch an entry from the database by its ID. returns a Task object or None
    def fetch_entry_by_id(self, taskID, user_id):
        with self.connection():
            self.cursor.execute(
                """
                SELECT * FROM tasks
                WHERE taskID = ? AND user_id = ?
                """,
                (taskID, user_id),
            )
            row = self.cursor.fetchone()

        if not row:
            return None

        current_task = task.Task(
            row[1], row[2], row[3], int(row[4]),
            row[5], row[6], bool(row[7]), row[8],
        )
        current_task.taskID = int(row[0])
        return current_task

    # toggle the completion status of an entry
    def toggle_entry_completion(self, taskID, user_id):
        with self.connection():
            self.cursor.execute(
                """
                SELECT is_complete FROM tasks
                WHERE taskID = ? AND user_id = ?
                """,
                (taskID, user_id),
            )
            row = self.cursor.fetchone()

            if row is not None:
                self.execute(
                    """
                    UPDATE tasks
                    SET is_complete = ?
                    WHERE taskID = ? AND user_id = ?
                    """,
                    (int(not bool(row[0])), taskID, user_id),
                )

    def get_username_by_id(self, user_id):
        with self.connection():
            self.cursor.execute(
                "SELECT username FROM users WHERE userID = ?",
                (user_id,),
            )
            row = self.cursor.fetchone()

        return row[0] if row else None

    def compare_token(self, candidate_token):
        if not candidate_token:
            return None

        candidate_hash = hashlib.sha256(
            candidate_token.encode("utf-8")
        ).hexdigest()

        with self.connection():
            self.cursor.execute(
                """
                SELECT user_id, token_hash
                FROM sessions
                WHERE expires_at > ?
                """,
                (int(time.time()),),
            )

            for user_id, stored_hash in self.cursor.fetchall():
                if hmac.compare_digest(candidate_hash, stored_hash):
                    return user_id

        return None

    def restore_session(self):
        token = keyring.get_password(
            KEYRING_SERVICE,
            KEYRING_ACCOUNT,
        )

        user_id = self.compare_token(token)

        if user_id is None and token:
            try:
                keyring.delete_password(
                    KEYRING_SERVICE,
                    KEYRING_ACCOUNT,
                )
            except keyring.errors.PasswordDeleteError:
                pass

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

    def get_tasks_for_user(self, user_id):
        """Return all tasks belonging to a user."""
        if user_id is None:
            return []

        self.open()

        try:
            self.cursor.execute(
                """
                SELECT taskID, title, dateAdded, dateDue, priority,
                       category, details, is_complete, user_id
                FROM tasks
                WHERE user_id = ?
                ORDER BY dateDue ASC, taskID ASC
                """,
                (user_id,)
            )

            tasks = []

            for row in self.cursor.fetchall():
                current_task = task.Task(
                    row[1], row[2], row[3], int(row[4]),
                    row[5], row[6], bool(row[7]), row[8]
                )
                current_task.taskID = row[0]
                tasks.append(current_task)

            return tasks
        finally:
            self.close()

    def authenticate_user(self, username, password):
        with self.connection():
            self.cursor.execute(
                """
                SELECT userID, password
                FROM users
                WHERE username = ?
                """,
                (username,),
            )
            result = self.cursor.fetchone()

        if result is None:
            return None

        user_id, stored_password = result

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password,
        ):
            return user_id

        return None

    def create_session(self, user_id):
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        expires_at = int(time.time()) + SESSION_DURATION

        with self.connection():
            self.execute(
                "DELETE FROM sessions WHERE user_id = ?",
                (user_id,),
            )
            self.execute(
                """
                INSERT INTO sessions
                    (user_id, token_hash, expires_at)
                VALUES (?, ?, ?)
                """,
                (user_id, token_hash, expires_at),
            )

        keyring.set_password(
            KEYRING_SERVICE,
            KEYRING_ACCOUNT,
            token,
        )

        return token