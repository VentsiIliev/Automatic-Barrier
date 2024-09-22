import sqlite3
from contextlib import closing

from shared.repositories.BaseRepository import BaseRepository


class SQLAccessDeniedRepository(BaseRepository):
    def __init__(self, database_path):
        self.database_path = database_path

    def connect(self):
        return sqlite3.connect(self.database_path)

    def get(self, license_plate):
        with closing(self.connect()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM access_denied WHERE license_plate = ?", (license_plate,))
            return cursor.fetchall()

    def insert(self, license_plate, reason):
        with closing(self.connect()) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO access_denied (license_plate, reason) VALUES (?, ?)", (license_plate, reason))
            conn.commit()

    def delete(self, license_plate):
        with closing(self.connect()) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM access_denied WHERE license_plate = ?", (license_plate,))
            conn.commit()
