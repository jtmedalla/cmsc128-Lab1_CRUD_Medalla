from data.task import Priority, Task
from frontend import main_window, task_entry


def test_task_card_creation():
    root = main_window.MainWindow()
    task_card = task_entry.TaskCard(master=root)
    assert isinstance(task_card, task_entry.TaskCard)
    root.mainloop()

test_task_card_creation()