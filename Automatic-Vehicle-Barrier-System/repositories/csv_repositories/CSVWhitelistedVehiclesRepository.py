from model.Vehicle import Vehicle
from model.access_events.AccessEvent import AccessEvent
from model.access_events.AccessLevel import AccessLevel
from repositories.csv_repositories.Constants import WHITELISTED_VEHICLES_FIELDS, REGISTRATION_NUMBER, OWNER, \
    ACCESS_LEVEL, EVENT_TYPE, DATE, TIME, DIRECTION
from repositories.csv_repositories.BaseCSVRepository import BaseCSVRepository


class CSVWhitelistedVehiclesRepository(BaseCSVRepository):
    def __init__(self, file_path):
        super().__init__(file_path, WHITELISTED_VEHICLES_FIELDS)

    def get_all(self):
        vehicles = []
        for row in self._read_rows():
            # Create an event from the row
            registration_number = row[REGISTRATION_NUMBER]
            owner = row[OWNER]
            access_level = AccessLevel(int(row[ACCESS_LEVEL]))
            vehicle = Vehicle(registration_number, owner, access_level)
            # Append the event to the events list
            vehicles.append(vehicle)
        return vehicles

    def get(self, license_plate):
        vehicle = None
        for row in self._read_rows():
            if row[REGISTRATION_NUMBER] == license_plate:
                vehicle = Vehicle(row[REGISTRATION_NUMBER], row[OWNER], AccessLevel(int(row[ACCESS_LEVEL])))
                break
        return vehicle

    def insert(self, vehicle):
        if self.get(vehicle) is None:
            super().insert(**{REGISTRATION_NUMBER: vehicle.registration_number, OWNER: vehicle.owner, ACCESS_LEVEL: vehicle.access_level})

    def delete(self, vehicle):
        super().delete(vehicle.registration_number)
