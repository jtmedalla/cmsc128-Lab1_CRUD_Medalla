import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from tkcalendar import DateEntry

from api.sqlite3_api import SQLiteConn
from frontend.task_entry import TaskCard


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ToDo List Application")
        self.geometry("600x720")
        self.resizable(False, True)

        self.db = SQLiteConn()
        self.db.open()
        self.filter_controls = {}

        self.initialize_display()

    def initialize_display(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        add_task_button = ttk.Button(
            self,
            text="Add Task",
            command=self.add_task
        )
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

    def create_task_filters(self, parent, completed):
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(3, weight=1)

        tasks = self.db.fetch_all_entries() or []
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
        priority_filter.current(0)
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
        sort_dropdown.current(0)
        sort_dropdown.grid(
            row=2, column=1, padx=10, pady=10, sticky="ew"
        )

        self.filter_controls[parent] = (
            tag_filter,
            priority_filter,
            sort_dropdown,
            completed
        )

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

        scroll_frame = ttk.Frame(parent)
        scroll_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )
        scroll_frame.columnconfigure(0, weight=1)
        scroll_frame.rowconfigure(0, weight=1)

        canvas = tk.Canvas(scroll_frame, highlightthickness=1, highlightbackground="black")
        scrollbar = ttk.Scrollbar(
            scroll_frame,
            orient="vertical",
            command=canvas.yview
        )
        task_frame = ttk.Frame(canvas)

        task_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=task_frame,
            anchor="nw"
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                canvas_window,
                width=event.width
            )
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        return task_frame

    def categorize_tasks(self):
        self.refresh_tasks(self.ongoing_tab)
        self.refresh_tasks(self.completed_tab)

    def refresh_tasks(self, parent):
        tag_filter, priority_filter, sort_dropdown, completed = (
            self.filter_controls[parent]
        )

        tasks = self.db.fetch_all_entries() or []

        tasks = [
            current_task
            for current_task in tasks
            if current_task.is_complete == completed
        ]

        selected_tag = tag_filter.get()
        if selected_tag != "All Tags":
            tasks = [
                current_task
                for current_task in tasks
                if current_task.category == selected_tag
            ]

        selected_priority = priority_filter.get()
        if selected_priority != "All Priorities":
            tasks = [
                current_task
                for current_task in tasks
                if getattr(
                    current_task.priority,
                    "name",
                    str(current_task.priority)
                ) == selected_priority
            ]

        sort_option = sort_dropdown.get()

        if sort_option == "Date Added":
            tasks.sort(key=lambda current_task: current_task.dateAdded)
        elif sort_option == "Date Due":
            tasks.sort(key=lambda current_task: current_task.dateDue)
        elif sort_option == "Priority":
            tasks.sort(
                key=lambda current_task: getattr(
                    current_task.priority,
                    "value",
                    current_task.priority
                )
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

        task_frame = (
            self.ongoing_tasks_frame
            if parent == self.ongoing_tab
            else self.completed_tasks_frame
        )

        self.display_tasks(task_frame, tasks)

    def display_tasks(self, parent, tasks):
        for widget in parent.winfo_children():
            widget.destroy()

        parent.columnconfigure(0, weight=1)

        for row, current_task in enumerate(tasks):
            completion = getattr(
                current_task,
                "is_complete",
                getattr(current_task, "is_complete", False)
            )

            match current_task.priority:
                case 0:
                    priority_text = "LOW"
                case 1:
                    priority_text = "MED"
                case 2:
                    priority_text = "HIGH"
                case _:
                    raise RuntimeError(f"Invalid priority value: {current_task.priority}")

            task_card = TaskCard(
                parent,
                id=current_task.taskID,
                title=current_task.title,
                dateAdded=current_task.dateAdded,
                dateDue=current_task.dateDue,
                priority=priority_text,
                category=current_task.category,
                details=current_task.details,
                completion=completion,
                db=self.db,
                on_change=self.categorize_tasks,
                on_delete=self.show_undo_toast
            )

            task_card.grid(
                row=row,
                column=0,
                padx=10,
                pady=10,
                sticky="ew"
            )

    def add_task(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Task")
        dialog.transient(self)
        dialog.grab_set()

        fields = {}

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

            self.db.add_entry(
                title=title,
                dateAdded=date_added,
                dateDue=date_due,
                priority=priority,
                category=category,
                details=details,
                completion=False
            )

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

    def undo_delete(self, deleted_task):
        self.db.add_entry(
            title=deleted_task["title"],
            dateAdded=deleted_task["dateAdded"],
            dateDue=deleted_task["dateDue"],
            priority=deleted_task["priority"],
            category=deleted_task["category"],
            details=deleted_task["details"],
            completion=deleted_task["completion"]
        )

        self.close_undo_toast()
        self.categorize_tasks()

    def close_undo_toast(self):
        if hasattr(self, "undo_toast") and self.undo_toast.winfo_exists():
            self.undo_toast.destroy()

        if hasattr(self, "undo_after_id"):
            self.after_cancel(self.undo_after_id)
            del self.undo_after_id

        self.categorize_tasks()

