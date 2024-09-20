from abc import ABC, abstractmethod
import csv
import os

from repositories.BaseRepository import BaseRepository


class BaseCSVRepository(BaseRepository):
    def __init__(self, file_path, fieldnames):
        self.file_path = file_path
        self.fieldnames = fieldnames
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        # os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            print("Creating file", self.file_path)
            with open(self.file_path, mode='w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()

    def _read_rows(self):
        rows = []
        with open(self.file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(row)
        return rows

    def _write_rows(self, rows):
        print("writing rows")
        with open(self.file_path, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def clear(self):
        """Clear all records (optional)."""
        self._write_rows([])

    def get(self, query):
        """Retrieve rows based on a query matching a specific field."""
        return [row for row in self._read_rows() if row[self.fieldnames[0]] == query]

    def insert(self, **kwargs):
        """Insert a new row with the given keyword arguments."""
        print("Inserting")
        rows = self._read_rows()
        rows.append(kwargs)
        self._write_rows(rows)

    def delete(self, query):
        """Delete rows matching a specific query."""
        rows = [row for row in self._read_rows() if row[self.fieldnames[0]] != query]
        self._write_rows(rows)

    def update(self, rows):
        """Update rows with the given rows."""
        self._write_rows(rows)
