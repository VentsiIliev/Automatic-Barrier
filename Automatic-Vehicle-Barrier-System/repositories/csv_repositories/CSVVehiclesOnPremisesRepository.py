from repositories.csv_repositories.Constants import VEHICLES_ON_PREMISES_FIELDS, REGISTRATION_NUMBER
from repositories.csv_repositories.BaseCSVRepository import BaseCSVRepository


class CSVVehiclesOnPremisesRepository(BaseCSVRepository):
    def __init__(self, file_path):
        super().__init__(file_path, VEHICLES_ON_PREMISES_FIELDS)

    def get_all(self):
        """Retrieve all registration numbers currently on premises."""
        df = self._read_rows()
        return df[REGISTRATION_NUMBER].tolist()  # Directly return the list of registration numbers

    def insert(self, registration_number):
        """Insert a new registration number."""
        super().insert(**{REGISTRATION_NUMBER: registration_number})

    def get(self, registration_number):
        """Retrieve a specific registration number."""
        df = self._read_rows()
        row = df[df[REGISTRATION_NUMBER] == registration_number]
        return row[REGISTRATION_NUMBER].values[0] if not row.empty else None
