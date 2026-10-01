import os
import sys

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QApplication

from api.sqlite3_api import SQLiteConn
from data import user_session
from frontend.frontend import (
    ForgotPasswordWindow,
    LoginGUI,
    MainApp,
    SignUpWindow,
)


class Application:
    user_logout = Signal()
    user_signup = Signal(str, str)  # username, password

    def __init__(self):
        self.todo_window = None
        self.user_session = None

        database_path = os.path.join(
            os.path.dirname(__file__),
            "data",
            "todolist.db",
        )
        database_exists = os.path.exists(database_path)

        self.db = SQLiteConn()
        self.db.open()

        self.app = QApplication([])

        self.login_window = LoginGUI(self.db)
        self.login_window.login_successful.connect(self.show_main_app)
        self.login_window.signup_requested.connect(
            self.show_create_account_window
        )
        self.login_window.forgot_password_requested.connect(
            self.show_forgot_password_window
        )

        self.db.close()

        if database_exists:
            if self.login_window.user_id is None:
                self.login_window.show()
            else:
                self.show_main_app(self.login_window.user_id)
        else:
            self.show_create_account_window()

        sys.exit(self.app.exec())


    @Slot(int)
    def show_main_app(self, user_id=None):
        if self.todo_window is not None:
            self.todo_window.activateWindow()
            return

        user_id = user_id or self.login_window.user_id
        self.user_session = user_session.UserSession(user_id, self.db)

        self.login_window.close()

        self.todo_window = MainApp(self.user_session)
        self.todo_window.log_out.connect(self.show_login_window)
        self.todo_window.show()

    @Slot()
    def show_login_window(self):
        self.db.logout()

        if self.todo_window is not None:
            self.todo_window.close()
            self.todo_window = None

        if self.user_session is not None:
            self.user_session.end_session()
            self.user_session = None

        self.login_window = LoginGUI(self.db)
        self.login_window.clear_credentials()

        self.login_window.login_successful.connect(
            self.show_main_app
        )
        self.login_window.signup_requested.connect(
            self.show_create_account_window
        )
        self.login_window.forgot_password_requested.connect(
            self.show_forgot_password_window
        )

        self.login_window.show()

    @Slot()
    def successful_signup(self, username, password):
        self.db.open()
        user_id = self.db.authenticate_user(username, password)
        self.db.close()

        if user_id is not None:
            self.show_login_window()

    @Slot()
    def show_create_account_window(self):
        self.login_window.hide()

        self.create_account_window = SignUpWindow(self.db)
        self.create_account_window.signup_successful.connect(
            self.show_login_window
        )
        self.create_account_window.closed.connect(
            self.login_window.show
        )
        self.create_account_window.show()


    @Slot()
    def show_forgot_password_window(self):
        self.login_window.hide()

        self.forgot_password_window = ForgotPasswordWindow(self.db)
        self.forgot_password_window.status_message.connect(
            self.show_login_status_message
        )
        self.forgot_password_window.closed.connect(
            self.login_window.show
        )
        self.forgot_password_window.show()


    @Slot(str, int)
    def show_login_status_message(self, message, timeout):
        self.login_window.ui.statusbar.showMessage(message, timeout)


if __name__ == "__main__":
    Application()

