from api import sqlite3_api


class UserSession:
    def __init__(self, user_id, db_connection=None):
        self.user_id = user_id
        self.is_active = True
        self.db_connection = db_connection if db_connection else sqlite3_api.SQLiteConn()
        self.username = self.get_username()

    def end_session(self):
        self.user_id = None
        self.is_active = False

    def get_username(self):
        if self.user_id is None:
            return None
        self.db_connection.open()
        username = self.db_connection.get_username_by_id(self.user_id)
        self.db_connection.close()
        return username