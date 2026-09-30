from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QMainWindow

from api import sqlite3_api
from data import user_session
from frontend import login_window, todolist_window


class LoginGUI(QMainWindow):
    login_successful = Signal(int)

    def __init__(self, db_connection=None):
        super().__init__()
        self.ui = login_window.Ui_login_window()
        self.ui.setupUi(self)
        self.db_connection = db_connection if db_connection else sqlite3_api.SQLiteConn()
        self.user_id = None

        if self.db_connection.conn is not None:
            self.user_id = self.db_connection.restore_session()
            self.db_connection.close()

            if self.user_id is not None:
                self.login_successful.emit(self.user_id)
                #TODO: open the main application window for the user with user_id
                print(f"Restored session for user_id: {self.user_id}")

        # initialize UI functionality
        self.ui.btn_login.clicked.connect(self.login_clicked)
        self.ui.btn_signup.clicked.connect(self.signup_clicked)
        
    @Slot()
    def login_clicked(self):
        username = self.ui.line_username.text()
        password = self.ui.line_password.text()

        db = self.db_connection

        db.open()

        self.user_id = db.authenticate_user(username, password)

        if self.user_id is not None:
            db.create_session(self.user_id)
            self.login_successful.emit(self.user_id)
            self.closeEvent(None)  
        else:
            self.ui.statusbar.showMessage("Login failed. Please check your username and password.", 5000)
        db.close()

    @Slot()
    def signup_clicked(self):
        username = self.ui.line_username.text()
        password = self.ui.line_password.text()

        db = self.db_connection

        db.open()
        if db.add_user(username, password):
            self.ui.statusbar.showMessage("Signup successful! You can now log in.", 5000)
        else:
            self.ui.statusbar.showMessage("Signup failed. Username may already exist.", 5000)
        db.close()

    def closeEvent(self, event):
        if self.user_id is not None and self.db_connection.conn is not None:
            self.db_connection.close()
            self.close()



class MainApp(QMainWindow):
    def __init__(self, user_session):
        super().__init__()
        self.ui = todolist_window.Ui_todolist_window()
        self.ui.setupUi(self)
        self.user_session = user_session
        self.db_connection = user_session.db_connection

        self.initialize_content()

    def initialize_content(self):
        self.ui.lbl_welcome.setText(f"Welcome, {self.user_session.username}!")
        self.ui.btn_acc_settings.clicked.connect(self.account_settings_clicked)


    @Slot()
    def account_settings_clicked(self):
        pass



        