from admin_dashboard.model.Vehicle import Vehicle
from core_system.model.access_events.AccessLevel import AccessLevel
from shared.repositories.csv_repositories.Constants import WHITELISTED_VEHICLES_FIELDS, REGISTRATION_NUMBER, OWNER, ACCESS_LEVEL
from shared.repositories.csv_repositories.BaseCSVRepository import BaseCSVRepository


class CSVWhitelistedVehiclesRepository(BaseCSVRepository):
    def __init__(self, file_path):
        super().__init__(file_path, WHITELISTED_VEHICLES_FIELDS)

    def get_all(self):
        df = self._read_rows()
        vehicles = [
            Vehicle(row[REGISTRATION_NUMBER], row[OWNER], AccessLevel(int(row[ACCESS_LEVEL])))
            for _, row in df.iterrows()
        ]
        return vehicles

    def get(self, license_plate):
        df = self._read_rows()
        row = df[df[REGISTRATION_NUMBER] == license_plate]
        if not row.empty:
            return Vehicle(row[REGISTRATION_NUMBER].values[0], row[OWNER].values[0], AccessLevel(int(row[ACCESS_LEVEL].values[0])))
        return None

    def insert(self, vehicle):
        print("Inserting vehicle")
        if self.get(vehicle.registration_number) is None:
            super().insert(
                **{
                    REGISTRATION_NUMBER: vehicle.registration_number,
                    OWNER: vehicle.owner,
                    ACCESS_LEVEL: vehicle.access_level
                }
            )

    def delete(self, registration_number):
        super().delete(registration_number)

    def update(self, vehicle: Vehicle):
        print("Updating")
        df = self._read_rows()
        df.loc[df[REGISTRATION_NUMBER] == vehicle.registration_number, [OWNER, ACCESS_LEVEL]] = vehicle.owner, vehicle.access_level
        self._write_rows(df)
