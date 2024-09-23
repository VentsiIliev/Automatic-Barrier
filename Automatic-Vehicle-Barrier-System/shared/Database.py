import os

from admin_dashboard.settings import Settings
from shared.AccessEventType import AccessEventType
from shared.CSVFileName import CSVFileName
from shared.repositories.csv_repositories.CSVAccessDeniedRepository import CSVAccessDeniedRepository
from shared.repositories.csv_repositories.CSVAccessGrantedRepository import CSVAccessGrantedRepository
from shared.repositories.csv_repositories.CSVVehiclesOnPremisesRepository import CSVVehiclesOnPremisesRepository
from shared.repositories.csv_repositories.CSVWhitelistedVehiclesRepository import CSVWhitelistedVehiclesRepository
from shared.repositories.csv_repositories.CSVUsersRepository import CSVUsersRepository


class Database:
    """A class to manage the database and repositories."""
    DATABASE_DIRECTORY = "database"

    def __init__(self, db_name):
        self.db_name = db_name
        self.access_denied_repo = CSVAccessDeniedRepository(os.path.join(f"{self.DATABASE_DIRECTORY}\\{CSVFileName.ACCESS_DENIED.value}"))
        self.access_granted_repo = CSVAccessGrantedRepository(os.path.join(f"{self.DATABASE_DIRECTORY}\\{CSVFileName.ACCESS_GRANTED.value}"))
        self.vehicles_on_premises_repo = CSVVehiclesOnPremisesRepository(os.path.join(f"{self.DATABASE_DIRECTORY}\\{CSVFileName.VEHICLES_ON_PREMISES.value}"))
        self.whitelisted_vehicles_repo = CSVWhitelistedVehiclesRepository(os.path.join(f"{self.DATABASE_DIRECTORY}\\{CSVFileName.WHITELISTED_VEHICLES.value}"))
        self.users_repo = CSVUsersRepository(os.path.join(f"{self.DATABASE_DIRECTORY}\\{CSVFileName.USERS.value}"))

    def get_repo(self, repo):
        """Return the repository object for the specified repository."""
        if repo == CSVFileName.ACCESS_GRANTED.strip_extension():
            return self.access_granted_repo
        elif repo == CSVFileName.ACCESS_DENIED.strip_extension():
            return self.access_denied_repo
        elif repo == CSVFileName.VEHICLES_ON_PREMISES.strip_extension():
            return self.vehicles_on_premises_repo
        elif repo == CSVFileName.WHITELISTED_VEHICLES.strip_extension():
            return self.whitelisted_vehicles_repo
        elif repo == CSVFileName.USERS.strip_extension():
            return self.users_repo
        else:
            raise ValueError(f"Invalid repository specified.{repo}")

    # def get_data(self, repo, filters=None):
    #     """Retrieve data from the specified repository."""
    #     if repo == 'granted':
    #         return self.access_granted_repo.get(filters)
    #     elif repo == 'denied':
    #         return self.access_denied_repo.get(filters)
    #     elif repo == 'vehicles':
    #         return self.vehicles_on_premises_repo.get_all()
    #     elif repo == 'whitelisted':
    #         return self.whitelisted_vehicles_repo.get(filters)
    #     else:
    #         raise ValueError("Invalid repository specified.")

    def log_event(self, event):
        """Log the event to the appropriate repository."""
        if event.type == AccessEventType.GRANTED:
            self.access_granted_repo.insert(
                event_type=event.type.value,
                date=event.time.strftime('%Y-%m-%d'),
                time=event.time.strftime('%H:%M:%S'),
                registration_number=event.registration_number,
                direction=event.direction,
                owner=event.owner  # Assuming the event has an owner attribute
            )
        elif event.type == AccessEventType.DENIED:
            self.access_denied_repo.insert(
                event_type=event.type.value,
                date=event.time.strftime('%Y-%m-%d'),
                time=event.time.strftime('%H:%M:%S'),
                registration_number=event.registration_number,
                direction=event.direction,
                owner=event.owner  # Assuming the event has an owner attribute
            )
        else:
            raise ValueError("Invalid event type")
