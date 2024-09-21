from abc import ABC, abstractmethod
import os
import pandas as pd
from repositories import DataFiltering
from repositories.BaseRepository import BaseRepository


class BaseCSVRepository(BaseRepository):
    def __init__(self, file_path, fieldnames):
        self.file_path = file_path
        self.fieldnames = fieldnames
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            print("Creating file", self.file_path)
            pd.DataFrame(columns=self.fieldnames).to_csv(self.file_path, index=False)

    def _read_rows(self):
        print(f"Reading rows from: {self.file_path}")
        df = pd.read_csv(self.file_path)
        print(df.head())  # Print the first few rows to inspect the structure
        return df

    def _write_rows(self, df):
        df.to_csv(self.file_path, index=False)

    def clear(self):
        """Clear all records (optional)."""
        pd.DataFrame(columns=self.fieldnames).to_csv(self.file_path, index=False)

    def get(self, query):
        """Retrieve rows based on a query matching a specific field."""
        df = self._read_rows()
        return df[df[self.fieldnames[0]] == query]

    def get_data(self, filters=None):
        """Get data with optional filters."""
        df = self._read_rows()
        if filters:
            df = DataFiltering.filterData(df, filters)
        return df

    def insert(self, **kwargs):
        """Insert a new row with the given keyword arguments."""
        print("Inserting")
        df = self._read_rows()
        df = df.append(kwargs, ignore_index=True)
        self._write_rows(df)

    def delete(self, query):
        """Delete rows matching a specific query."""
        df = self._read_rows()  # Read rows as DataFrame
        df = df[df[self.fieldnames[0]] != query]  # Filter out the row(s) to delete
        self._write_rows(df)  # Write the updated DataFrame back to CSV

    def update(self, df):
        """Update rows with the given DataFrame."""
        self._write_rows(df)
