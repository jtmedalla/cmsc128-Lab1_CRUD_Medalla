from api import sqlite3_api
from data import task


def test_conn():
    # test that the connection to the database is established
    db = sqlite3_api.SQLiteConn()
    db.open()

    assert db.conn is not None
    assert db.cursor is not None

    db.close()

def test_add_entry():
    # test that an entry can be added to the database
    db = sqlite3_api.SQLiteConn()
    db.open()

    task1 = task.Task("Test Task", "2024-06-01", task.Priority.HIGH, "Test Category", "Test Description", False)

    task1.taskID = db.add_entry(task1.title, task1.date, task1.priority, task1.category, task1.description, task1.isComplete)
    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))

    result = db.cursor.fetchone()
    assert result is not None
    assert result[1] == task1.title
    assert result[2] == task1.date
    assert result[3] == task1.priority.value
    assert result[4] == task1.category
    assert result[5] == task1.description

    db.close()

def test_remove_entry():
    # test that an entry can be removed from the database
    db = sqlite3_api.SQLiteConn()
    db.open()

    task1 = task.Task("Test Task", "2024-06-01", task.Priority.HIGH, "Test Category", "Test Description", False)

    task1.taskID = db.add_entry(task1.title, task1.date, task1.priority, task1.category, task1.description, task1.isComplete)
    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))
    result = db.cursor.fetchone()
    assert result is not None

    task1.taskID = result[0]
    db.remove_entry(result[0])
    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))
    result = db.cursor.fetchone()
    assert result is None

    db.close()

def test_update_entry():
    # test that an entry can be updated in the database
    db = sqlite3_api.SQLiteConn()
    db.open()

    task1 = task.Task("Test Task", "2024-06-01", task.Priority.HIGH, "Test Category", "Test Description", False)

    task1.taskID = db.add_entry(task1.title, task1.date, task1.priority, task1.category, task1.description, task1.isComplete)
    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))
    result = db.cursor.fetchone()
    assert result is not None

    new_title = "Updated Task"
    new_date = "2024-06-02"
    new_priority = task.Priority.LOW
    new_category = "Updated Category"
    new_description = "Updated Description"
    new_completion = True

    db.update_entry(result[0], title=new_title, date=new_date, priority=new_priority, category=new_category, description=new_description, completion=new_completion)
    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (result[0],))
    updated_result = db.cursor.fetchone()

    assert updated_result is not None
    assert updated_result[1] == new_title
    assert updated_result[2] == new_date
    assert updated_result[3] == new_priority.value
    assert updated_result[4] == new_category
    assert updated_result[5] == new_description
    assert updated_result[6] == int(new_completion)

    db.close()

def test_fetch_all_entries():
    # test that all entries can be fetched from the database
    db = sqlite3_api.SQLiteConn()
    db.open()

    task1 = task.Task("Test Task 1", "2024-06-01", task.Priority.HIGH, "Test Category 1", "Test Description 1", False)
    task2 = task.Task("Test Task 2", "2024-06-02", task.Priority.LOW, "Test Category 2", "Test Description 2", False)

    task1.taskID = db.add_entry(task1.title, task1.date, task1.priority, task1.category, task1.description, task1.isComplete)
    task2.taskID = db.add_entry(task2.title, task2.date, task2.priority, task2.category, task2.description, task2.isComplete)

    results = db.fetch_all_entries()
    assert len(results) >= 2

    titles = [result.title for result in results]
    assert task1.title in titles
    assert task2.title in titles

    db.close()

def test_fetch_entry_by_id():
    # test that an entry can be fetched from the database by its ID
    db = sqlite3_api.SQLiteConn()
    db.open()

    task1 = task.Task("Test Task", "2024-06-01", task.Priority.HIGH, "Test Category", "Test Description", False)

    task1.taskID = db.add_entry(task1.title, task1.date, task1.priority, task1.category, task1.description, task1.isComplete)
    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))
    result = db.cursor.fetchone()
    assert result is not None

    assert result[0] == task1.taskID

    fetched_result = db.fetch_entry_by_id(result[0])
    assert fetched_result is not None
    assert fetched_result.taskID == task1.taskID
    assert fetched_result.title == task1.title
    assert fetched_result.date == task1.date
    assert fetched_result.priority == task1.priority.value
    assert fetched_result.category == task1.category
    assert fetched_result.description == task1.description

    db.close()

def test_toggle_completion():
    # test that the completion status of an entry can be toggled
    db = sqlite3_api.SQLiteConn()
    db.open()

    task1 = task.Task("Test Task", "2024-06-01", task.Priority.HIGH, "Test Category", "Test Description", False)

    task1.taskID = db.add_entry(task1.title, task1.date, task1.priority, task1.category, task1.description, task1.isComplete)
    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (task1.taskID,))
    result = db.cursor.fetchone()
    assert result is not None

    initial_completion_status = result[6]
    db.toggle_entry_completion(result[0])
    db.cursor.execute("SELECT * FROM tasks WHERE taskID = ?", (result[0],))
    updated_result = db.cursor.fetchone()

    assert updated_result is not None
    assert updated_result[6] != initial_completion_status

    db.close()
