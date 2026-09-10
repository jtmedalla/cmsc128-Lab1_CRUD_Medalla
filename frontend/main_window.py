import tkinter as tk
from datetime import date, datetime
from tkinter import messagebox, ttk

from tkcalendar import DateEntry

from api.sqlite3_api import SQLiteConn
from data import task as task_model
from frontend.task_entry import TaskCard


class MainWindow(tk.Tk):
    def __init__(self):
        # initialize the main window
        super().__init__()
        self.title("ToDo List Application")
        self.geometry("600x720")
        self.resizable(False, True)

        self.db = SQLiteConn()
        self.db.open()
        self.filter_controls = {}

        # grab the tasks from the database and store them in a local variable
        self.tasks = self.db.fetch_all_entries() or []

        self.task_cards = {}

        self.initialize_display()

    def initialize_display(self):
        # decorate the main window with buttons and tabs upon opening
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        add_task_button = ttk.Button(
            self,
            text="Add Task",
            command=self.add_task
        )

        # used for the tab separation of ongoing and completed tasks
        tab_control = ttk.Notebook(self)

        self.ongoing_tab = ttk.Frame(tab_control)
        self.completed_tab = ttk.Frame(tab_control)

        tab_control.add(self.ongoing_tab, text="Ongoing Tasks")
        tab_control.add(self.completed_tab, text="Completed Tasks")

        add_task_button.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )
        tab_control.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.ongoing_tasks_frame = self.create_task_filters(
            self.ongoing_tab,
            completed=False
        )
        self.completed_tasks_frame = self.create_task_filters(
            self.completed_tab,
            completed=True
        )

        self.categorize_tasks()

    # for creating the filter and sort options for the tasks
    def create_task_filters(self, parent, completed):
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(3, weight=1)

        # store all the entries from the database to a local variable
        tasks = self.tasks

        tags = sorted({
            current_task.category
            for current_task in tasks
            if current_task.category
        })

        ttk.Label(parent, text="Filter by Tag:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        tag_filter = ttk.Combobox(
            parent,
            values=["All Tags", *tags],
            state="readonly"
        )
        tag_filter.current(0)
        tag_filter.grid(
            row=0, column=1, padx=10, pady=10, sticky="ew"
        )

        ttk.Label(parent, text="Filter by Priority:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )

        priority_filter = ttk.Combobox(
            parent,
            values=["All Priorities", "LOW", "MED", "HIGH"],
            state="readonly"
        )
        priority_filter.current(0)  # set default selection to "All Priorities"
        priority_filter.grid(
            row=1, column=1, padx=10, pady=10, sticky="ew"
        )

        ttk.Label(parent, text="Sort by:").grid(
            row=2, column=0, padx=10, pady=10, sticky="w"
        )

        sort_dropdown = ttk.Combobox(
            parent,
            values=[
                "Date Added",
                "Date Due",
                "Priority",
                "Tag (A-Z)",
                "Tag (Z-A)"
            ],
            state="readonly"
        )
        sort_dropdown.current(1) # set default value to "Date Due"
        sort_dropdown.grid(
            row=2, column=1, padx=10, pady=10, sticky="ew"
        )

        # store the filter controls for later use
        self.filter_controls[parent] = (
            tag_filter,
            priority_filter,
            sort_dropdown,
            completed
        )

        # bind the filter and sort controls to the refresh_tasks method
        tag_filter.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_tasks(parent)
        )
        priority_filter.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_tasks(parent)
        )
        sort_dropdown.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_tasks(parent)
        )

        # frame containing the tasks with a scrollbar for navigation
        scroll_frame = tk.Frame(parent, highlightthickness=1, highlightbackground="black")
        scroll_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew",
            
        )
        scroll_frame.columnconfigure(0, weight=1)
        scroll_frame.rowconfigure(0, weight=1)

        # create a canvas and a scrollbar for the scroll frame
        canvas = tk.Canvas(scroll_frame, )
        scrollbar = ttk.Scrollbar(
            scroll_frame,
            orient="vertical",
            command=canvas.yview
        )
        task_frame = ttk.Frame(canvas)

        # bind the canvas and scrollbar to the task frame for scrolling functionality
        task_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # create a window inside the canvas to hold the task frame
        canvas_window = canvas.create_window(
            (0, 0),
            window=task_frame,
            anchor="nw"
        )

        # bind the canvas to the scrollbar for scrolling functionality
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                canvas_window,
                width=event.width
            )
        )

        # configure the scrollbar to update the canvas view when scrolled
        canvas.configure(yscrollcommand=scrollbar.set)

        # place the canvas and scrollbar in the scroll frame using grid layout
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        return task_frame

    def categorize_tasks(self):
        # categorize the tasks according to their completion status and refresh the display
        self.refresh_tasks(self.ongoing_tab)
        self.refresh_tasks(self.completed_tab)

    # used to refresh the display of tasks based on the selected filters and sorting options
    def refresh_tasks(self, parent):
        
        tag_filter, priority_filter, sort_dropdown, completed = (
            self.filter_controls[parent]
        )

        # filter tasks based on their completion status
        tasks = [
            current_task
            for current_task in self.tasks
            if bool(getattr(
                current_task,
                "is_complete",
                getattr(current_task, "is_complete", False)
            )) == completed
        ]

        # filter tasks based on the selected tag and priority
        selected_tag = tag_filter.get()
        if selected_tag != "All Tags":
            tasks = [
                current_task
                for current_task in tasks
                if current_task.category == selected_tag
            ]

        # filter tasks based on the selected priority
        selected_priority = priority_filter.get()
        if selected_priority != "All Priorities":
            tasks = [
                current_task
                for current_task in tasks
                # check if the priority attribute has a name attribute (for Enum) or use a mapping for integer values
                # TODO: refactor this to be more consistent in using enums or integers for priority representation
                if (
                    current_task.priority.name
                    if hasattr(current_task.priority, "name")
                    else {
                        0: "LOW",
                        1: "MED",
                        2: "HIGH"
                    }.get(
                        self.priority_sort_value(current_task.priority)
                    )
                ) == selected_priority
            ]

        # sort the tasks based on the selected sorting option
        sort_option = sort_dropdown.get()
        if sort_option == "Date Added":
            tasks.sort(key=lambda current_task: current_task.dateAdded)
        elif sort_option == "Date Due":
            tasks.sort(key=lambda current_task: current_task.dateDue)
        elif sort_option == "Priority":
            tasks.sort(
                key=lambda current_task: self.priority_sort_value(
                    current_task.priority
                ), reverse=True
            )
        elif sort_option == "Tag (A-Z)":
            tasks.sort(
                key=lambda current_task: current_task.category.lower()
            )
        elif sort_option == "Tag (Z-A)":
            tasks.sort(
                key=lambda current_task: current_task.category.lower(),
                reverse=True
            )

        # determine which task frame to display the tasks in based on the parent tab
        task_frame = (
            self.ongoing_tasks_frame
            if parent == self.ongoing_tab
            else self.completed_tasks_frame
        )

        # display the filtered and sorted tasks in the appropriate task frame
        self.display_tasks(task_frame, tasks)

    def update_filter_values(self):
        tags = sorted({
            current_task.category
            for current_task in self.tasks
            if current_task.category
        })

        for tag_filter, _, _, _ in self.filter_controls.values():
            current_tag = tag_filter.get()
            tag_filter["values"] = ["All Tags", *tags]

            if current_tag in tag_filter["values"]:
                tag_filter.set(current_tag)
            else:
                tag_filter.current(0)

    def task_changed(self, changed_card):
        for current_task in self.tasks:
            if current_task.taskID == changed_card.id:
                current_task.title = changed_card.title
                current_task.dateDue = changed_card.dateDue
                current_task.priority = changed_card.priority
                current_task.category = changed_card.category
                current_task.details = changed_card.details
                current_task.is_complete = changed_card.completion
                break

        self.update_filter_values()
        self.categorize_tasks()


    def display_tasks(self, parent, tasks):
        # Keep cards separate for ongoing and completed tabs.
        card_group = self.task_cards.setdefault(parent, {})

        visible_ids = {
            current_task.taskID
            for current_task in tasks
        }

        for task_id, card in card_group.items():
            if task_id not in visible_ids:
                card.grid_remove()

        for row, current_task in enumerate(tasks):
            task_id = current_task.taskID
            card = card_group.get(task_id)

            if card is None or not card.winfo_exists():
                card = TaskCard(
                    parent,
                    id=task_id,
                    title=current_task.title,
                    dateAdded=current_task.dateAdded,
                    dateDue=current_task.dateDue,
                    priority=current_task.priority,
                    category=current_task.category,
                    details=current_task.details,
                    completion=current_task.is_complete,
                    db=self.db,
                    on_change=self.task_changed,
                    on_delete=self.show_undo_toast
                )
                card_group[task_id] = card

            card.grid(
                row=row,
                column=0,
                padx=10,
                pady=10,
                sticky="ew"
            )

    def add_task(self):
        # create a pop-up menu for adding a new task
        dialog = tk.Toplevel(self)
        dialog.title("Add Task")
        dialog.transient(self)
        dialog.grab_set()

        fields = {}

        # display the fields for the task attributes in the pop-up menu
        for row, label in enumerate(
            ["Title", "Date Due", "Category", "Details"]
        ):
            ttk.Label(dialog, text=f"{label}:").grid(
                row=row,
                column=0,
                padx=10,
                pady=5,
                sticky="w"
            )

            if label == "Details":
                widget = tk.Text(dialog, height=4, width=35)
            elif label == "Date Due":
                widget = DateEntry(
                    dialog,
                    width=33,
                    date_pattern="yyyy-mm-dd",
                    mindate=date.today()
                )
            else:
                widget = ttk.Entry(dialog, width=35)

            widget.grid(
                row=row,
                column=1,
                columnspan=3,
                padx=10,
                pady=5,
                sticky="ew"
            )
            fields[label] = widget

        ttk.Label(dialog, text="Priority:").grid(
            row=4,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        priority_box = ttk.Combobox(
            dialog,
            values=["LOW", "MED", "HIGH"],
            state="readonly"
        )
        priority_box.current(0)
        priority_box.grid(
            row=4,
            column=1,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew"
        )

        # run when the user selects "Save Task"
        def save_task():
            title = fields["Title"].get().strip()
            date_added = date.today().isoformat()
            date_due = fields["Date Due"].get_date().isoformat()
            category = fields["Category"].get().strip()
            details = fields["Details"].get("1.0", tk.END).strip()

            if not title or not category:
                messagebox.showerror(
                    "Invalid Task",
                    "Title and category are required.",
                    parent=dialog
                )
                return

            priority = {
                "LOW": 0,
                "MED": 1,
                "HIGH": 2
            }[priority_box.get()]

            new_task = task_model.Task(
                title,
                date_added,
                date_due,
                task_model.Priority(priority),
                category,
                details,
                False
            )

            new_task.taskID = self.db.add_entry(
                title=title,
                dateAdded=date_added,
                dateDue=date_due,
                priority=priority,
                category=category,
                details=details,
                completion=False
            )

            self.tasks.append(new_task)
            self.update_filter_values()

            dialog.destroy()
            self.categorize_tasks()

        ttk.Button(
            dialog,
            text="Save",
            command=save_task
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="ew"
        )

        ttk.Button(
            dialog,
            text="Cancel",
            command=dialog.destroy
        ).grid(
            row=5,
            column=2,
            columnspan=2,
            padx=10,
            pady=5,
            sticky="ew"
        )

        dialog.columnconfigure(1, weight=1)

    def show_undo_toast(self, deleted_task):
        if hasattr(self, "undo_toast") and self.undo_toast.winfo_exists():
            self.undo_toast.destroy()

        if hasattr(self, "undo_after_id"):
            self.after_cancel(self.undo_after_id)

        self.undo_toast = tk.Toplevel(self)
        self.undo_toast.overrideredirect(True)
        self.undo_toast.attributes("-topmost", True)

        toast_frame = tk.Frame(
            self.undo_toast,
            bg="#323232",
            padx=12,
            pady=8
        )
        toast_frame.pack()

        tk.Label(
            toast_frame,
            text="Task deleted",
            fg="white",
            bg="#323232"
        ).pack(side="left", padx=(0, 12))

        tk.Button(
            toast_frame,
            text="Undo",
            command=lambda: self.undo_delete(deleted_task)
        ).pack(side="right")

        self.update_idletasks()

        x = self.winfo_rootx() + self.winfo_width() - self.undo_toast.winfo_reqwidth() - 20
        y = self.winfo_rooty() + self.winfo_height() - self.undo_toast.winfo_reqheight() - 20

        self.undo_toast.geometry(f"+{x}+{y}")

        self.undo_after_id = self.after(
            5000,
            self.close_undo_toast
        )

        self.tasks = [
            current_task
            for current_task in self.tasks
            if current_task.taskID != deleted_task["id"]
        ]

        self.update_filter_values()
        self.categorize_tasks()

    def undo_delete(self, deleted_task):
        task_id = self.db.add_entry(
            title=deleted_task["title"],
            dateAdded=deleted_task["dateAdded"],
            dateDue=deleted_task["dateDue"],
            priority=deleted_task["priority"],
            category=deleted_task["category"],
            details=deleted_task["details"],
            completion=deleted_task["completion"]
        )

        restored_task = task_model.Task(
            deleted_task["title"],
            deleted_task["dateAdded"],
            deleted_task["dateDue"],
            deleted_task["priority"],
            deleted_task["category"],
            deleted_task["details"],
            deleted_task["completion"]
        )
        restored_task.taskID = task_id
        self.tasks.append(restored_task)

        self.update_filter_values()
        self.close_undo_toast()
        self.categorize_tasks()

    def close_undo_toast(self):
        if hasattr(self, "undo_toast") and self.undo_toast.winfo_exists():
            self.undo_toast.destroy()

        if hasattr(self, "undo_after_id"):
            self.after_cancel(self.undo_after_id)
            del self.undo_after_id

    # used to get the value of the priority for sorting purposes, regardless of whether it's an Enum or an integer
    # TODO: refactor code in the future to be more consistent in using enums or integers for priority representation
    @staticmethod
    def priority_sort_value(priority):
        value = getattr(priority, "value", priority)

        if isinstance(value, str):
            return {
                "LOW": 0,
                "MED": 1,
                "HIGH": 2
            }.get(value.upper(), 0)

        return int(value)
