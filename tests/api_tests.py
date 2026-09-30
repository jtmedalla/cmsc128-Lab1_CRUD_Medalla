import uuid

import bcrypt

from api import sqlite3_api
from data import task


def create_test_owner(db):
    username = "test_owner"
    password = "test_password"

    db.add_user(username, password)

    db.cursor.execute(
        "SELECT userID FROM users WHERE username = ?",
        (username,)
    )
    return db.cursor.fetchone()[0]


def create_test_session(db):
    username = f"test_owner_{uuid.uuid4().hex}"
    password = "test_password"

    assert db.add_user(username, password) is True

    user_id = db.authenticate_user(username, password)
    assert user_id is not None

    db.create_session(user_id)
    assert db.restore_session() == user_id

    return user_id


def add_test_task(db, task_obj, user_id):
    return db.add_entry(
        task_obj.title,
        task_obj.dateAdded,
        task_obj.dateDue,
        task_obj.priority,
        task_obj.category,
        task_obj.details,
        task_obj.is_complete,
        user_id
    )


def test_conn():
    db = sqlite3_api.SQLiteConn()
    db.open()

    assert db.conn is not None
    assert db.cursor is not None

    db.close()

def test_add_user():
    db = sqlite3_api.SQLiteConn()
    db.open()

    username = "test_user_add"
    password = "test_password"
    bytes_password = password.encode('utf-8')

    db.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    db.conn.commit()

    db.add_user(username, password)

    db.cursor.execute(
        "SELECT username, password FROM users WHERE username = ?",
        (username,)
    )
    result = db.cursor.fetchone()

    assert bcrypt.checkpw(bytes_password, result[1])

    db.close()


def test_user_login():
    db = sqlite3_api.SQLiteConn()
    db.open()

    username = f"test_user_{uuid.uuid4().hex}"
    password = "test_password"

    assert db.add_user(username, password) is True
    assert db.authenticate_user(username, password) is not None
    assert db.authenticate_user(username, "incorrect_password") is None
    assert db.authenticate_user("unknown_user", password) is None

    db.close()


def test_add_entry():
    db = sqlite3_api.SQLiteConn()
    db.open()
    user_id = create_test_owner(db)

    task1 = task.Task(
        "Test Task",
        "2024-05-01",
        "2024-06-01",
        task.Priority.HIGH,
        "Test Category",
        "Test details",
        False
    )

    task1.taskID = add_test_task(db, task1, user_id)

    db.cursor.execute(
        "SELECT * FROM tasks WHERE taskID = ? AND user_id = ?",
        (task1.taskID, user_id,)
    )
    result = db.cursor.fetchone()

    assert result is not None
    assert result[1] == task1.title
    assert result[2] == task1.dateAdded
    assert result[3] == task1.dateDue
    assert result[4] == task1.priority.value
    assert result[5] == task1.category
    assert result[6] == task1.details
    assert result[7] == int(task1.is_complete)
    assert result[8] == user_id

    db.close()


def test_remove_entry():
    db = sqlite3_api.SQLiteConn()
    db.open()

    task1 = task.Task(
        "Test Task",
        "2024-05-01",
        "2024-06-01",
        task.Priority.HIGH,
        "Test Category",
        "Test details",
        False,
        create_test_owner(db)
    )

    task1.taskID = db.add_entry(
        task1.title,
        task1.dateAdded,
        task1.dateDue,
        task1.priority,
        task1.category,
        task1.details,
        task1.is_complete,
        task1.user_id
    )

    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ? AND user_id = ?", (task1.taskID, task1.user_id))
    result = db.cursor.fetchone()
    assert result is not None

    db.remove_entry(result[0], task1.user_id)

    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ? AND user_id = ?", (task1.taskID, task1.user_id))
    assert db.cursor.fetchone() is None

    db.close()


def test_update_entry():
    db = sqlite3_api.SQLiteConn()
    db.open()

    user_id = create_test_owner(db)

    task1 = task.Task(
        "Test Task",
        "2024-05-01",
        "2024-06-01",
        task.Priority.HIGH,
        "Test Category",
        "Test details",
        False
    )

    task1.taskID = add_test_task(db, task1, user_id)

    new_title = "Updated Task"
    new_date_added = "2024-05-02"
    new_date_due = "2024-06-02"
    new_priority = task.Priority.LOW
    new_category = "Updated Category"
    new_details = "Updated details"
    new_completion = True

    db.update_entry(
        task1.taskID,
        title=new_title,
        dateAdded=new_date_added,
        dateDue=new_date_due,
        priority=new_priority,
        category=new_category,
        details=new_details,
        completion=new_completion,
        user_id=user_id
    )
    print(task1.taskID, user_id)
    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ? AND user_id = ?", (task1.taskID, user_id))
    updated_result = db.cursor.fetchone()

    assert updated_result is not None
    assert updated_result[1] == new_title
    assert updated_result[2] == new_date_added
    assert updated_result[3] == new_date_due
    assert updated_result[4] == new_priority.value
    assert updated_result[5] == new_category
    assert updated_result[6] == new_details
    assert updated_result[7] == int(new_completion)
    assert updated_result[8] == user_id

    db.close()


def test_fetch_all_entries():
    db = sqlite3_api.SQLiteConn()
    db.open()

    user_id = create_test_owner(db)

    task1 = task.Task(
        "Test Task 1",
        "2024-05-01",
        "2024-06-01",
        task.Priority.HIGH,
        "Test Category 1",
        "Test details 1",
        False
    )
    task2 = task.Task(
        "Test Task 2",
        "2024-05-02",
        "2024-06-02",
        task.Priority.LOW,
        "Test Category 2",
        "Test details 2",
        False
    )

    task1.taskID = add_test_task(db, task1, user_id)
    task2.taskID = add_test_task(db, task2, user_id)

    results = db.fetch_all_entries(user_id)

    assert len(results) >= 2
    assert task1.taskID in [result.taskID for result in results]
    assert task2.taskID in [result.taskID for result in results]

    db.close()


def test_fetch_entry_by_id():
    db = sqlite3_api.SQLiteConn()
    db.open()

    user_id = create_test_owner(db)

    task1 = task.Task(
        "Test Task",
        "2024-05-01",
        "2024-06-01",
        task.Priority.HIGH,
        "Test Category",
        "Test details",
        False
    )

    task1.taskID = add_test_task(db, task1, user_id)

    fetched_result = db.fetch_entry_by_id(task1.taskID, user_id)

    assert fetched_result is not None
    assert fetched_result.taskID == task1.taskID
    assert fetched_result.title == task1.title
    assert fetched_result.dateAdded == task1.dateAdded
    assert fetched_result.dateDue == task1.dateDue
    assert fetched_result.priority == task1.priority.value
    assert fetched_result.category == task1.category
    assert fetched_result.details == task1.details
    assert fetched_result.is_complete == task1.is_complete
    assert fetched_result.user_id == user_id

    db.close()


def test_toggle_completion():
    db = sqlite3_api.SQLiteConn()
    db.open()

    user_id = create_test_owner(db)

    task1 = task.Task(
        "Test Task",
        "2024-05-01",
        "2024-06-01",
        task.Priority.HIGH,
        "Test Category",
        "Test details",
        False
    )

    task1.taskID = add_test_task(db, task1, user_id)

    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ? AND user_id = ?", (task1.taskID, user_id))
    result = db.cursor.fetchone()
    assert result is not None

    initial_completion_status = result[7]
    db.toggle_entry_completion(task1.taskID, user_id)

    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))
    updated_result = db.cursor.fetchone()

    assert updated_result is not None
    assert updated_result[7] != initial_completion_status

    db.close()


def test_session_lifecycle():
    db = sqlite3_api.SQLiteConn()
    db.open()

    user_id = create_test_session(db)

    assert db.restore_session() == user_id

    db.logout()
    assert db.restore_session() is None

    db.close()