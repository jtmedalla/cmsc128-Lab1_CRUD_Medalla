from PySide6.QtWidgets import QMainWindow

from frontend.login_window import Ui_login_window


class LoginGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_login_window()
        self.ui.setupUi(self)