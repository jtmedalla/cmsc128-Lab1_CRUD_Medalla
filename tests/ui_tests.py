import os
from types import SimpleNamespace

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from data.task import Task
from frontend.frontend import AddTaskWindow, MainApp, TaskCard


@pytest.fixture(scope="session")
def qapp():
    application = QApplication.instance() or QApplication([])
    yield application


def make_task(
    task_id,
    title,
    date_due,
    category="General",
    priority=1,
    is_complete=False,
):
    current_task = Task(
        title,
        "2026-01-01",
        date_due,
        priority,
        category,
        f"Details for {title}",
        is_complete,
        7,
    )
    current_task.taskID = task_id
    return current_task


class StubDatabase:
    def __init__(self, tasks=None):
        self.tasks = list(tasks or [])
        self.fetch_count = 0
        self.added_tasks = []
        self.updated_tasks = []

    def get_tasks_for_user(self, user_id):
        self.fetch_count += 1
        return list(self.tasks)

    def add_task(self, **task_fields):
        self.added_tasks.append(task_fields)

    def update_entry(self, taskID, completion, user_id):
        self.updated_tasks.append((taskID, completion, user_id))
        for current_task in self.tasks:
            if current_task.taskID == taskID:
                current_task.is_complete = completion


def make_session(database):
    return SimpleNamespace(
        user_id=7,
        username="Test User",
        db_connection=database,
    )


def cards_in_layout(layout, task_cards):
    return [
        item.widget()
        for index in range(layout.count())
        if (item := layout.itemAt(index)).widget() in task_cards.values()
    ]


def test_task_card_displays_task_and_emits_completion(qapp):
    current_task = make_task(1, "Write tests", "2026-05-01", "School")
    card = TaskCard(current_task)
    changes = []
    card.completion_changed.connect(
        lambda task_id, is_complete: changes.append((task_id, is_complete))
    )

    assert card.ui.lbl_placeholder_title.text() == "Write tests"
    assert card.ui.lbl_placeholder_category.text() == "School"

    card.ui.chkbox_is_complete.setChecked(True)
    assert changes == [(1, True)]


def test_main_app_filters_and_sorts_cached_cards(qapp):
    tasks = [
        make_task(1, "Alpha", "2026-12-01", "Work"),
        make_task(2, "Beta", "2026-01-01", "Home"),
    ]
    database = StubDatabase(tasks)
    window = MainApp(make_session(database))
    ongoing_tab = window.ui.tab_ongoing_tasks
    layout = window.task_containers[ongoing_tab].task_layout
    original_cards = dict(window.task_cards)

    assert [
        card.task_id
        for card in cards_in_layout(layout, window.task_cards)
    ] == [2, 1]

    category_index = window.ui.combo_category.findData("Work")
    window.ui.combo_category.setCurrentIndex(category_index)
    assert not window.task_cards[1].isHidden()
    assert window.task_cards[2].isHidden()

    sort_index = window.ui.combo_sort.findData("title")
    window.ui.combo_sort.setCurrentIndex(sort_index)
    assert [
        card.task_id
        for card in cards_in_layout(layout, window.task_cards)
    ] == [1, 2]
    assert window.task_cards == original_cards
    assert database.fetch_count == 1


def test_completion_moves_card_to_completed_tab(qapp):
    database = StubDatabase([make_task(3, "Ship feature", "2026-08-01")])
    window = MainApp(make_session(database))
    card = window.task_cards[3]

    card.ui.chkbox_is_complete.setChecked(True)

    completed_tab = window.ui.tab_completed_tasks
    assert database.updated_tasks == [(3, True, 7)]
    assert window.task_cards[3] is card
    assert card.parentWidget() is window.task_containers[completed_tab]
    assert database.fetch_count == 2


def test_add_task_validates_and_submits_form(qapp):
    database = StubDatabase()
    window = AddTaskWindow(make_session(database))

    window.ui.btn_add_task.click()
    assert window.ui.statusbar.currentMessage() == "Task title is required."
    assert database.added_tasks == []

    window.ui.line_title.setText("Review pull request")
    window.ui.line_category.setText("Work")
    window.ui.textEdit.setPlainText("Check the error handling")
    window.ui.cmb_priority.setCurrentIndex(2)
    window.ui.btn_add_task.click()

    assert database.added_tasks[0]["title"] == "Review pull request"
    assert database.added_tasks[0]["category"] == "Work"
    assert (
        database.added_tasks[0]["details"]
        == "Check the error handling"
    )
    assert database.added_tasks[0]["priority"] == 3
    assert database.added_tasks[0]["user_id"] == 7
