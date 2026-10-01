from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QMainWindow

from api import sqlite3_api
from frontend import account_settings_window, login_window, todolist_window


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
    log_out = Signal()

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
        self.setEnabled(False)

        self.account_settings_window = AccountSettingsWindow(self.user_session)
        self.account_settings_window.status_message.connect(
            self.show_status_message
        )
        self.account_settings_window.updated_successfully.connect(
            self.refresh_account_details
        )
        self.account_settings_window.closed.connect(
            self.account_settings_closed
        )
        self.account_settings_window.logout.connect(
            self.user_logged_out
        )
        self.account_settings_window.show()

    @Slot()
    def account_settings_closed(self):
        self.setEnabled(True)
        self.activateWindow()

    @Slot()
    def refresh_account_details(self):
        self.user_session.username = self.user_session.get_username()
        self.ui.lbl_welcome.setText(f"Welcome, {self.user_session.username}!")

    @Slot()
    def user_logged_out(self):
        self.log_out.emit()
        self.close()

    @Slot(str, int)
    def show_status_message(self, message, timeout):
        self.ui.statusbar.showMessage(message, timeout)


class AccountSettingsWindow(QMainWindow):
    status_message = Signal(str, int)
    updated_successfully = Signal()
    closed = Signal()
    logout = Signal()

    def __init__(self, user_session):
        super().__init__()
        self.ui = account_settings_window.Ui_account_settings_window()
        self.ui.setupUi(self)
        self.user_session = user_session
        self.db_connection = user_session.db_connection

        self.ui.line_update_usrname.setText(self.user_session.username)
        self.ui.btn_update_dets.clicked.connect(self.update_password_clicked)
        self.ui.btn_update_cancel.clicked.connect(self.close)
        self.ui.btn_logout.clicked.connect(self.logout_clicked)

    @Slot()
    def update_password_clicked(self):
        username = self.ui.line_update_usrname.text()
        old_password = self.ui.line_curr_pwd.text()
        new_password = self.ui.line_new_pwd.text()

        db = self.db_connection
        db.open()

        is_authenticated = db.authenticate_user(
            self.user_session.username,
            old_password
        )

        if not is_authenticated:
            self.status_message.emit("Old password is incorrect.", 5000)
            db.close()
            return

        if db.update_user_info(self.user_session.user_id, username, new_password):
            self.status_message.emit(
                "Account updated successfully!",
                5000
            )
            self.updated_successfully.emit()

            self.close()
        else:
            self.status_message.emit(
                "Failed to update account details.",
                5000
            )

        db.close()

    @Slot()
    def logout_clicked(self):
        self.logout.emit()
        self.close()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)



