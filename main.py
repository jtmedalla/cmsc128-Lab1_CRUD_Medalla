import sys

from PySide6.QtWidgets import QApplication

from frontend.frontend import LoginGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoginGUI()
    window.show()

    sys.exit(app.exec())