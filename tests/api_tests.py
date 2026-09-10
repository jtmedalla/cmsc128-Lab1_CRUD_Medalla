from api import sqlite3_api
from data import task


def test_conn():
    db = sqlite3_api.SQLiteConn()
    db.open()

    assert db.conn is not None
    assert db.cursor is not None

    db.close()


def test_add_entry():
    db = sqlite3_api.SQLiteConn()
    db.open()

    task1 = task.Task(
        "Test Task",
        "2024-05-01",
        "2024-06-01",
        task.Priority.HIGH,
        "Test Category",
        "Test details",
        False
    )

    task1.taskID = db.add_entry(
        task1.title,
        task1.dateAdded,
        task1.dateDue,
        task1.priority,
        task1.category,
        task1.details,
        task1.is_complete
    )

    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))
    result = db.cursor.fetchone()

    assert result is not None
    assert result[1] == task1.title
    assert result[2] == task1.dateAdded
    assert result[3] == task1.dateDue
    assert result[4] == task1.priority.value
    assert result[5] == task1.category
    assert result[6] == task1.details
    assert result[7] == int(task1.is_complete)

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
        False
    )

    task1.taskID = db.add_entry(
        task1.title,
        task1.dateAdded,
        task1.dateDue,
        task1.priority,
        task1.category,
        task1.details,
        task1.is_complete
    )

    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))
    result = db.cursor.fetchone()
    assert result is not None

    db.remove_entry(result[0])

    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))
    assert db.cursor.fetchone() is None

    db.close()


def test_update_entry():
    db = sqlite3_api.SQLiteConn()
    db.open()

    task1 = task.Task(
        "Test Task",
        "2024-05-01",
        "2024-06-01",
        task.Priority.HIGH,
        "Test Category",
        "Test details",
        False
    )

    task1.taskID = db.add_entry(
        task1.title,
        task1.dateAdded,
        task1.dateDue,
        task1.priority,
        task1.category,
        task1.details,
        task1.is_complete
    )

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
        completion=new_completion
    )

    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))
    updated_result = db.cursor.fetchone()

    assert updated_result is not None
    assert updated_result[1] == new_title
    assert updated_result[2] == new_date_added
    assert updated_result[3] == new_date_due
    assert updated_result[4] == new_priority.value
    assert updated_result[5] == new_category
    assert updated_result[6] == new_details
    assert updated_result[7] == int(new_completion)

    db.close()


def test_fetch_all_entries():
    db = sqlite3_api.SQLiteConn()
    db.open()

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

    task1.taskID = db.add_entry(
        task1.title, task1.dateAdded, task1.dateDue, task1.priority,
        task1.category, task1.details, task1.is_complete
    )
    task2.taskID = db.add_entry(
        task2.title, task2.dateAdded, task2.dateDue, task2.priority,
        task2.category, task2.details, task2.is_complete
    )

    results = db.fetch_all_entries()

    assert len(results) >= 2
    assert task1.title in [result.title for result in results]
    assert task2.title in [result.title for result in results]

    db.close()


def test_fetch_entry_by_id():
    db = sqlite3_api.SQLiteConn()
    db.open()

    task1 = task.Task(
        "Test Task",
        "2024-05-01",
        "2024-06-01",
        task.Priority.HIGH,
        "Test Category",
        "Test details",
        False
    )

    task1.taskID = db.add_entry(
        task1.title,
        task1.dateAdded,
        task1.dateDue,
        task1.priority,
        task1.category,
        task1.details,
        task1.is_complete
    )

    fetched_result = db.fetch_entry_by_id(task1.taskID)

    assert fetched_result is not None
    assert fetched_result.taskID == task1.taskID
    assert fetched_result.title == task1.title
    assert fetched_result.dateAdded == task1.dateAdded
    assert fetched_result.dateDue == task1.dateDue
    assert fetched_result.priority == task1.priority.value
    assert fetched_result.category == task1.category
    assert fetched_result.details == task1.details

    db.close()


def test_toggle_completion():
    db = sqlite3_api.SQLiteConn()
    db.open()

    task1 = task.Task(
        "Test Task",
        "2024-05-01",
        "2024-06-01",
        task.Priority.HIGH,
        "Test Category",
        "Test details",
        False
    )

    task1.taskID = db.add_entry(
        task1.title,
        task1.dateAdded,
        task1.dateDue,
        task1.priority,
        task1.category,
        task1.details,
        task1.is_complete
    )

    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))
    result = db.cursor.fetchone()
    assert result is not None

    initial_completion_status = result[7]
    db.toggle_entry_completion(task1.taskID)

    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))
    updated_result = db.cursor.fetchone()

    assert updated_result is not None
    assert updated_result[7] != initial_completion_status

    db.close()
