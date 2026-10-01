import sys

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QApplication

from api.sqlite3_api import SQLiteConn
from data import user_session
from frontend.frontend import LoginGUI, MainApp


class Application:
    user_logout = Signal()

    def __init__(self):

        self.db = SQLiteConn()
        self.db.open()

        self.app = QApplication([])

        self.login_window = LoginGUI(self.db)
        self.login_window.login_successful.connect(self.show_main_app)

        self.db.close()

        if self.login_window.user_id is None:
            self.login_window.show()
        else:
            self.show_main_app()

        sys.exit(self.app.exec())


    @Slot()
    def show_main_app(self):
        # grab the user_id from the login window and create a UserSession
        self.db.open()
        self.user_session = user_session.UserSession(self.login_window.user_id, self.db)
        self.db.close()

        self.login_window.close()

        self.todo_window = MainApp(self.user_session)
        self.todo_window.log_out.connect(self.show_login_window)
        self.todo_window.show()

    @Slot()
    def show_login_window(self):
        self.todo_window.close()
        self.db.open()
        self.user_session.end_session()
        self.db.logout()
        self.login_window = LoginGUI(self.db)
        self.login_window.login_successful.connect(self.show_main_app)
        self.login_window.show()
        self.db.close()


if __name__ == "__main__":
    Application()

