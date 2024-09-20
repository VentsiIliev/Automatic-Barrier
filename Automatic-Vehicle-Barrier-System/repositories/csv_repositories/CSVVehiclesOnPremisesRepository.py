from repositories.csv_repositories.Constants import VEHICLES_ON_PREMISES_FIELDS, REGISTRATION_NUMBER

from repositories.csv_repositories.BaseCSVRepository import BaseCSVRepository


class CSVVehiclesOnPremisesRepository(BaseCSVRepository):
    def __init__(self, file_path):
        super().__init__(file_path, VEHICLES_ON_PREMISES_FIELDS)

    def insert(self, registration_number):
        super().insert(**{REGISTRATION_NUMBER: registration_number})

    def get(self, registration_number):
        return super().get(registration_number)

    def get_all(self):
        events = []
        return [row[REGISTRATION_NUMBER] for row in self._read_rows()]
