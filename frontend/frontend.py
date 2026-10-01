from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QMainWindow

from api import sqlite3_api
from frontend import (
    account_settings_window,
    forgot_password_window,
    login_window,
    sign_up_window,
    todolist_window,
)

MIN_PASSWORD_LENGTH = 8


class LoginGUI(QMainWindow):
    login_successful = Signal(int)
    signup_requested = Signal()
    forgot_password_requested = Signal()

    def __init__(self, db_connection=None):
        super().__init__()
        self.ui = login_window.Ui_login_window()
        self.ui.setupUi(self)

        self.db_connection = (
            db_connection
            if db_connection
            else sqlite3_api.SQLiteConn()
        )
        
        self.user_id = self.db_connection.restore_session()

        self.ui.btn_login.clicked.connect(self.login_clicked)
        self.ui.btn_signup.clicked.connect(self.signup_clicked)
        self.ui.btn_forgot_password.clicked.connect(
            self.forgot_password_clicked
        )

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
            self.close()
        else:
            self.ui.statusbar.showMessage(
                "Login failed. Please check your username and password.",
                5000
            )

        db.close()

    def clear_credentials(self):
        self.user_id = None
        self.ui.line_username.clear()
        self.ui.line_password.clear()

    @Slot()
    def signup_clicked(self):
        self.clear_credentials()
        self.signup_requested.emit()

    @Slot()
    def forgot_password_clicked(self):
        self.forgot_password_requested.emit()

    def closeEvent(self, event):
        self.clear_credentials()
        super().closeEvent(event)



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
        username = self.ui.line_update_usrname.text().strip()
        old_password = self.ui.line_curr_pwd.text()
        new_password = self.ui.line_new_pwd.text()

        if new_password != "" and not valid_password(new_password):
            self.status_message.emit(
                "New password must be at least 8 characters long.",
                5000
            )
            return

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

        if username != self.user_session.username and db.username_exists(
            username,
            exclude_user_id=self.user_session.user_id
        ):
            self.status_message.emit(
                "Username already exists. Please choose another username.",
                5000
            )
            db.close()
            return

        if db.update_user_info(
            self.user_session.user_id,
            username,
            new_password
        ):
            self.status_message.emit(
                "Account updated successfully!",
                5000
            )
            self.updated_successfully.emit()

        db.close()
        self.close()

    @Slot()
    def logout_clicked(self):
        self.logout.emit()
        self.close()

    @Slot()
    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

class SignUpWindow(QMainWindow):
    signup_successful = Signal()
    closed = Signal()

    def __init__(self, db_connection=None):
        super().__init__()
        self._signup_completed = False

        self.ui = sign_up_window.Ui_create_account_window()
        self.ui.setupUi(self)

        self.db_connection = (
            db_connection
            if db_connection
            else sqlite3_api.SQLiteConn()
        )

        questions = sqlite3_api.SECURITY_QUESTIONS

        self.ui.combo_security_question_1.addItems(questions)
        self.ui.combo_security_question_2.addItems(questions)

        self.ui.btn_create_acc.clicked.connect(self.signup_clicked)
        self.ui.btn_cancel.clicked.connect(self.close)

    @Slot()
    def signup_clicked(self):
        username = self.ui.line_new_username.text().strip()
        password = self.ui.line_new_password.text()
        confirm_password = self.ui.line_confirm_password.text()

        question_1 = self.ui.combo_security_question_1.currentText()
        question_2 = self.ui.combo_security_question_2.currentText()

        answer_1 = self.ui.line_answer_1.text().strip()
        answer_2 = self.ui.line_answer_2.text().strip()

        if not all((
            username,
            password,
            confirm_password,
            answer_1,
            answer_2,
        )):
            self.ui.statusbar.showMessage(
                "All fields are required.",
                5000
            )
            return

        if not valid_password(password):
            self.ui.statusbar.showMessage(
                "Password must be at least 8 characters long.",
                5000
            )
            return

        if password != confirm_password:
            self.ui.statusbar.showMessage(
                "Passwords do not match.",
                5000
            )
            return

        if question_1 == question_2:
            self.ui.statusbar.showMessage(
                "Choose two different security questions.",
                5000
            )
            return

        if self.db_connection.username_exists(username):
            self.ui.statusbar.showMessage(
                "Username already exists.",
                5000
            )
            return

        created = self.db_connection.add_user(
            username,
            password,
            question_1,
            answer_1,
            question_2,
            answer_2,
        )

        if not created:
            self.ui.statusbar.showMessage(
                "Failed to create account.",
                5000
            )
            return

        self.ui.statusbar.showMessage(
            "Account created successfully.",
            5000
        )

        self._signup_completed = True
        self.signup_successful.emit()
        self.close()

    def closeEvent(self, event):
        if not self._signup_completed:
            self.closed.emit()

        super().closeEvent(event)

class ForgotPasswordWindow(QMainWindow):
    completed = Signal()
    closed = Signal()
    status_message = Signal(str, int)

    def __init__(self, db_connection=None):
        super().__init__()
        self.ui = forgot_password_window.Ui_forgot_password_window()
        self.ui.setupUi(self)

        self.db_connection = (
            db_connection
            if db_connection
            else sqlite3_api.SQLiteConn()
        )

        questions = sqlite3_api.SECURITY_QUESTIONS
        self.ui.combo_security_question_1.addItems(questions)
        self.ui.combo_security_question_2.addItems(questions)

        self.ui.line_username.editingFinished.connect(
            self.load_security_questions
        )
        self.ui.btn_submit.clicked.connect(self.reset_password)
        self.ui.btn_cancel.clicked.connect(self.close)

    @Slot()
    def load_security_questions(self):
        username = self.ui.line_username.text().strip()

        if not username:
            return

        questions = self.db_connection.get_security_questions(username)

        if questions is None:
            self.status_message.emit(
                "Username was not found.", 5000
            )
            return

        index_1 = self.ui.combo_security_question_1.findText(questions[0])
        index_2 = self.ui.combo_security_question_2.findText(questions[1])

        if index_1 >= 0:
            self.ui.combo_security_question_1.setCurrentIndex(index_1)

        if index_2 >= 0:
            self.ui.combo_security_question_2.setCurrentIndex(index_2)

    @Slot()
    def reset_password(self):
        username = self.ui.line_username.text().strip()
        answer_1 = self.ui.line_answer_1.text()
        answer_2 = self.ui.line_answer_2.text()
        new_password = self.ui.line_new_password.text()

        if not username or not answer_1 or not answer_2 or not new_password:
            self.ui.statusbar.showMessage(
                "All fields are required.",
                5000
            )
            return

        if not valid_password(new_password):
            self.ui.statusbar.showMessage(
                "New password must be at least 8 characters long.",
                5000
            )
            return

        success = self.db_connection.reset_password(
            username,
            answer_1,
            answer_2,
            new_password
        )

        if success:
            self.ui.statusbar.showMessage(
                "Account password reset successfully.",
                5000
            )
            self.completed.emit()
            self.close()
        else:
            self.ui.statusbar.showMessage(
                "Incorrect security answers.",
                5000
            )

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

def valid_password(password):
    return len(password) >= MIN_PASSWORD_LENGTH



