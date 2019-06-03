import sqlite3


class DBhandler:

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def db_connect(self):
        """Establish connection to the DB and return the cursor"""
        self.conn = sqlite3.connect(self.db_name)
        if self.conn is not None:
            self.cursor = self.conn.cursor()
            return True
        else:
            return False

    def db_insert_suggestion(self, data):
        query = "INSERT OR REPLACE INTO suggestion(name) VALUES (?)"
        if query:
            self.cursor.executemany(query, data)
            self.conn.commit()
            return True
        else:
            return False
