from enum import Enum


class CSVFileName(Enum):
    ACCESS_GRANTED = "access_granted.csv"
    ACCESS_DENIED = "access_denied.csv"
    USERS = "users.csv"
    WHITELISTED_VEHICLES = "whitelisted_vehicles.csv"
    VEHICLES_ON_PREMISES = "vehicles_on_premises.csv"

    def strip_extension(self):
        return self.value.replace('.csv', '')

