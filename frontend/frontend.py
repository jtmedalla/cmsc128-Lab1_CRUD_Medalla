from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

from frontend.login_window import Ui_login_window
import api.sqlite3_api as sqlite3_api


class LoginGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_login_window()
        self.ui.setupUi(self)

        # initialize UI functionality
        self.ui.btn_login.clicked.connect(self.login_clicked)
        self.ui.btn_signup.clicked.connect(self.signup_clicked)
        
    @Slot()
    def login_clicked(self):
        username = self.ui.line_username.text()
        password = self.ui.line_password.text()

        db = sqlite3_api.SQLiteConn()

        db.open()
        if db.user_login(username, password):
            self.ui.statusbar.showMessage("Login successful!", 5000)
        else:
            self.ui.statusbar.showMessage("Login failed. Please check your username and password.", 5000)
        db.close()

    @Slot()
    def signup_clicked(self):
        username = self.ui.line_username.text()
        password = self.ui.line_password.text()

        db = sqlite3_api.SQLiteConn()

        db.open()
        if db.add_user(username, password):
            self.ui.statusbar.showMessage("Signup successful! You can now log in.", 5000)
        else:
            self.ui.statusbar.showMessage("Signup failed. Username may already exist.", 5000)
        db.close()
        