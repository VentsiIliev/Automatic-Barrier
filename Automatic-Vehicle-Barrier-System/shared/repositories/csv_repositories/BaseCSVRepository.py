import os
import pandas as pd
from filelock import FileLock, Timeout
from shared.repositories import DataFiltering
from shared.repositories.BaseRepository import BaseRepository

# Define constants for print messages
LOCK_ACQUIRED_READING = "Lock acquired for reading: {}"
LOCK_RELEASED = "Lock released for {}"
LOCK_ACQUIRE_TIMEOUT_READING = "Could not acquire lock for reading: {} within the timeout period."
LOCK_ACQUIRED_WRITING = "Lock acquired for writing: {}"
LOCK_ACQUIRE_TIMEOUT_WRITING = "Could not acquire lock for writing: {} within the timeout period."

class BaseCSVRepository(BaseRepository):
    def __init__(self, file_path, fieldnames):
        self.file_path = file_path
        self.fieldnames = fieldnames
        self.lock_path = f"{file_path}.lock"  # Path for the lock file
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensure the CSV file exists, creating it if it does not."""
        with FileLock(self.lock_path, timeout=10):  # Timeout added
            if not os.path.exists(self.file_path):
                print("Creating file", self.file_path)
                pd.DataFrame(columns=self.fieldnames).to_csv(self.file_path, index=False)

    def _read_rows(self):
        """Read rows from the CSV file with a file lock."""
        try:
            with FileLock(self.lock_path, timeout=10):
                print(LOCK_ACQUIRED_READING.format(self.file_path))
                df = pd.read_csv(self.file_path)
                print(LOCK_RELEASED.format(self.file_path))
            return df
        except Timeout:
            print(LOCK_ACQUIRE_TIMEOUT_READING.format(self.file_path))
            return pd.DataFrame(columns=self.fieldnames)

    def _write_rows(self, df):
        """Write rows to the CSV file with a file lock."""
        try:
            with FileLock(self.lock_path, timeout=10):
                print(LOCK_ACQUIRED_WRITING.format(self.file_path))
                df.to_csv(self.file_path, index=False)
                print(LOCK_RELEASED.format(self.file_path))
        except Timeout:
            print(LOCK_ACQUIRE_TIMEOUT_WRITING.format(self.file_path))

    def clear(self):
        """Clear all records in the CSV file."""
        self._write_rows(pd.DataFrame(columns=self.fieldnames))

    def get(self, query):
        """Retrieve rows based on a query matching a specific field."""
        df = self._read_rows()
        return df[df[self.fieldnames[0]] == query]

    def get_data(self, filters=None):
        """Get data from the CSV file, with optional filtering."""
        df = self._read_rows()
        if filters:
            df = DataFiltering.filterData(df, filters)
        return df

    def insert(self, **kwargs):
        """Insert a new row into the CSV file."""
        df = self._read_rows()
        new_row = pd.DataFrame([kwargs])
        df = pd.concat([df, new_row], ignore_index=True)
        self._write_rows(df)

    def delete(self, query):
        """Delete rows matching a specific query."""
        df = self._read_rows()
        df = df[df[self.fieldnames[0]] != query]  # Filter out the rows to delete
        self._write_rows(df)

    def update(self, df):
        """Update rows by writing the given DataFrame."""
        self._write_rows(df)
