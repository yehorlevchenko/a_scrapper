import sqlite3
import logging
from itertools import product


class DBHandler:

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def db_connect(self):
        self.connection = sqlite3.connect(self.db_name)
        if self.connection:
            self.cursor = self.connection.cursor()
            return True
        else:
            return False

    def db_get_queries(self):
        if not self.connection:
            self.db_connect()
        self.cursor.execute("SELECT * FROM query")
        all_rows = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM query WHERE processed = 0")
        not_processed_rows = self.cursor.fetchall()

        if len(not_processed_rows) == len(all_rows):
            return all_rows
        elif 0 < len(not_processed_rows) < len(all_rows):
            return not_processed_rows
        else:
            q = "UPDATE query SET processed = 0"
            self.cursor.execute(q)
            self.connection.commit()
            return all_rows

    def db_insert_suggestion(self, records, query_name):
        if not self.connection:
            self.db_connect()

        q = f"UPDATE query SET processed = 1 WHERE name = '{query_name}'"
        self.cursor.execute(q)

        records = [(record[0], query_name) for record in records]
        records_q = "INSERT OR REPLACE INTO suggestion(name, suggestion_query) VALUES (?, ?)"
        if records:
            self.cursor.executemany(records_q, records)
            self.connection.commit()
            return True
        else:
            return False

    def db_populate(self):
        if not self.connection:
            self.db_connect()
        self.cursor.execute("SELECT Count(*) FROM query")
        query_count = self.cursor.fetchone()[0]
        if query_count == 0:
            alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                         'u', 'v', 'w', 'x', 'y', 'z']
            records = {"".join(i) for i in product(alphabets, repeat=3)}
            records = {(r, 0) for r in records}
            self.cursor.executemany("INSERT OR IGNORE INTO query(name, processed) VALUES (?, ?)", records)
            self.connection.commit()
        else:
            logging.info(f"Query table is already populated: {query_count} records.")
