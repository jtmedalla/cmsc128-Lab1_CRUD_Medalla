import sys

from PySide6.QtWidgets import QApplication

from api.sqlite3_api import SQLiteConn
from frontend.frontend import LoginGUI

if __name__ == "__main__":

    db = SQLiteConn()
    db.open()

    app = QApplication(sys.argv)

    window = LoginGUI(db)
    if window.user_id is None:
        window.show()
        sys.exit(app.exec())
    else:
        print(f"Restored session for user_id: {window.user_id}")

    