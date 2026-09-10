import tkinter as tk
import tkinter.ttk as ttk
from datetime import date, datetime
from tkinter import messagebox

from tkcalendar import DateEntry


class TaskCard(tk.Frame):
    def __init__(
        self,
        master=None,
        id=None,
        title=None,
        dateAdded=None,
        dateDue=None,
        priority=None,
        category=None,
        details=None,
        completion=False,
        db=None,
        on_change=None,
        on_delete=None
    ):
        super().__init__(master)

        self.id = id
        self.db = db
        self.on_change = on_change
        self.on_delete = on_delete
        self.completion = completion

        self.title = title
        self.dateAdded = dateAdded
        self.dateDue = dateDue
        self.priority = priority
        self.category = category
        self.details = details

        # frame settings
        self.config(
            relief="raised",
            borderwidth=2,
            padx=10,
            pady=10,
            highlightbackground="black",
            highlightthickness=1
        )

        self.create_widgets()

    def create_widgets(self):

        # create labels and entry fields for task attributes
        self.title_label = tk.Label(self, text="Title:")
        self.title_entry = tk.Entry(self)
        self.title_entry.insert(0, self.title or "")
        self.title_entry.config(state="readonly")

        self.date_added_label = tk.Label(self, text="Date Added:")
        self.date_added_entry = tk.Entry(self)
        self.date_added_entry.insert(0, self.dateAdded or "")
        self.date_added_entry.config(state="readonly")

        date_due_row = 1

        self.date_due_label = tk.Label(self, text="Due Date:")
        self.date_due_entry = tk.Entry(self)
        self.date_due_entry.insert(0, self.dateDue or "")
        self.date_due_entry.config(state="readonly")

        self.priority_label = tk.Label(self, text="Priority:")
        self.priority_entry = tk.Entry(self)
        self.priority_entry.insert(0, self.get_priority_name())
        self.priority_entry.config(state="readonly")

        self.category_label = tk.Label(self, text="Category:")
        self.category_entry = tk.Entry(self)
        self.category_entry.insert(0, self.category or "")
        self.category_entry.config(state="readonly")

        self.details_label = tk.Label(self, text="Details:")
        self.details_entry = tk.Text(self, height=4, width=30)
        self.details_entry.insert(tk.END, self.details or "")
        self.details_entry.config(state="disabled")

        fields = [
            (self.title_label, self.title_entry),
            (self.date_added_label, self.date_added_entry),
            (self.date_due_label, self.date_due_entry),
            (self.priority_label, self.priority_entry),
            (self.category_label, self.category_entry),
            (self.details_label, self.details_entry),
        ]

        for row, (label, entry) in enumerate(fields):
            label.grid(row=row, column=0, padx=5, pady=3, sticky="w")
            entry.grid(row=row, column=1, padx=5, pady=3, sticky="ew")

        self.edit_button = tk.Button(
            self,
            text="Edit",
            command=self.edit_task
        )
        self.edit_button.grid(row=0, column=2, padx=5, pady=8)

        self.delete_button = tk.Button(
            self,
            text="Delete",
            command=self.delete_task,
            background="#8b0000",
            foreground="white",
            activebackground="#ff0000",
            activeforeground="white"
        )
        self.delete_button.grid(row=1, column=2, padx=5, pady=8)

        self.complete_button = tk.Button(
            self,
            text="Mark Ongoing" if self.completion else "Mark Complete",
            command=self.mark_complete,
            background="#006400" if not self.completion else "#FFA500",
            activebackground="#4CAF50" if not self.completion else "#FFA500",
        )
        self.complete_button.grid(row=2, column=2, padx=5, pady=8)

        self.apply_card_color()

    def get_priority_name(self):
        if hasattr(self.priority, "name"):
            return self.priority.name

        try:
            return ["LOW", "MED", "HIGH"][int(self.priority)]
        except (ValueError, TypeError, IndexError):
            return str(self.priority)

    def get_card_color(self):
        try:
            due_date = self.dateDue

            if isinstance(due_date, datetime):
                due_date = due_date.date()
            elif isinstance(due_date, str):
                due_date = datetime.strptime(
                    due_date[:10],
                    "%Y-%m-%d"
                ).date()

            if due_date < date.today():
                return "gray"

        except (ValueError, TypeError):
            pass

        return {
            "HIGH": "#ff9999",
            "MED": "#fff2a8",
            "LOW": "#a8e6a3"
        }.get(self.get_priority_name(), "white")

    def apply_card_color(self):
        color = self.get_card_color()

        self.configure(bg=color)

        for widget in self.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=color)

    def set_editable(self, editable):
        entry_state = "normal" if editable else "readonly"

        for entry in (
            self.title_entry,
            self.date_added_entry,
            self.date_due_entry,
            self.priority_entry,
            self.category_entry
        ):
            entry.config(state=entry_state)

        self.details_entry.config(
            state="normal" if editable else "disabled"
        )

    def edit_task(self):
        editor = tk.Toplevel(self)
        editor.title("Edit Task")
        editor.transient(self.winfo_toplevel())
        editor.grab_set()

        fields = {}

        tk.Label(editor, text="Title:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        title_entry = tk.Entry(editor, width=35)
        title_entry.insert(0, self.title or "")
        title_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        fields["Title"] = title_entry

        tk.Label(editor, text="Date Due:").grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        date_due_entry = DateEntry(
            editor,
            width=32,
            date_pattern="yyyy-mm-dd",
            state="readonly",
            closecalendar=False
        )

        try:
            date_due_entry.set_date(
                datetime.strptime(
                    str(self.dateDue)[:10],
                    "%Y-%m-%d"
                ).date()
            )
        except (ValueError, TypeError):
            date_due_entry.set_date(date.today())

        date_due_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=5,
            sticky="ew"
        )

        tk.Label(editor, text="Category:").grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )
        category_entry = tk.Entry(editor, width=35)
        category_entry.insert(0, self.category or "")
        category_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        fields["Category"] = category_entry

        priority_row = 3

        tk.Label(editor, text="Priority:").grid(
            row=priority_row,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        priority_box = tk.StringVar(value=self.get_priority_name())
        priority_menu = ttk.Combobox(
            editor,
            values=["LOW", "MED", "HIGH"],
            state="readonly"
        )
        priority_menu.set(self.get_priority_name())
        priority_menu.grid(
            row=priority_row,
            column=1,
            padx=10,
            pady=5,
            sticky="ew"
        )

        details_row = priority_row + 1

        tk.Label(editor, text="Details:").grid(
            row=details_row,
            column=0,
            padx=10,
            pady=5,
            sticky="nw"
        )

        details_text = tk.Text(editor, width=35, height=5)
        details_text.insert(tk.END, self.details or "")
        details_text.grid(
            row=details_row,
            column=1,
            padx=10,
            pady=5,
            sticky="ew"
        )

        def save_changes():
            title = fields["Title"].get().strip()
            date_due = date_due_entry.get_date().isoformat()
            category = fields["Category"].get().strip()
            details = details_text.get("1.0", tk.END).strip()

            if not title or not date_due or not category:
                messagebox.showerror(
                    "Invalid Task",
                    "Title, due date, and category are required.",
                    parent=editor
                )
                return

            priority = {
                "LOW": 0,
                "MED": 1,
                "HIGH": 2
            }[priority_menu.get()]

            self.db.update_entry(
                self.id,
                title=title,
                dateDue=date_due,
                priority=priority,
                category=category,
                details=details
            )

            editor.destroy()

            if self.on_change:
                self.on_change()

        tk.Button(
            editor,
            text="Save Changes",
            command=save_changes
        ).grid(
            row=details_row + 1,
            column=0,
            columnspan=2,
            padx=10,
            pady=10
        )

        editor.columnconfigure(1, weight=1)

    def delete_task(self):
        confirmed = messagebox.askyesno(
            "Delete Task",
            "Are you sure you want to delete this task?",
            parent=self.winfo_toplevel()
        )

        if not confirmed:
            return

        deleted_task = {
            "id": self.id,
            "title": self.title,
            "dateAdded": self.dateAdded,
            "dateDue": self.dateDue,
            "priority": self.priority,
            "category": self.category,
            "details": self.details,
            "completion": self.completion
        }

        self.db.remove_entry(self.id)

        if self.on_delete:
            self.on_delete(deleted_task)
        elif self.on_change:
            self.on_change()

    def mark_complete(self):
        self.db.toggle_entry_completion(self.id)
        self.completion = not self.completion

        if self.on_change:
            self.on_change(self)