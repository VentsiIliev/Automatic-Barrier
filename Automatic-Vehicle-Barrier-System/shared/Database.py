import os

from admin_dashboard.Settings import Settings
from shared.AccessEventType import AccessEventType
from shared.repositories.csv_repositories.CSVAccessDeniedRepository import CSVAccessDeniedRepository
from shared.repositories.csv_repositories.CSVAccessGrantedRepository import CSVAccessGrantedRepository
from shared.repositories.csv_repositories.CSVVehiclesOnPremisesRepository import CSVVehiclesOnPremisesRepository
from shared.repositories.csv_repositories.CSVWhitelistedVehiclesRepository import CSVWhitelistedVehiclesRepository
from shared.repositories.csv_repositories.CSVUsersRepository import CSVUsersRepository


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.access_denied_repo = CSVAccessDeniedRepository(os.path.join("database\\access_denied.csv"))
        self.access_granted_repo = CSVAccessGrantedRepository(os.path.join("database\\access_granted.csv"))
        self.vehicles_on_premises_repo = CSVVehiclesOnPremisesRepository(os.path.join("database"
                                                                                      "\\vehicles_on_premises.csv"))
        self.whitelisted_vehicles_repo = CSVWhitelistedVehiclesRepository(os.path.join("database"
                                                                                       "\\whitelisted_vehicles.csv"))
        self.users_repo = CSVUsersRepository(os.path.join("database\\users.csv"))

    def get_repo(self, repo):
        """Return the repository object for the specified repository."""
        if repo == Settings.ACCESS_GRANTED_CSV:
            return self.access_granted_repo
        elif repo == Settings.ACCESS_DENIED_CSV:
            return self.access_denied_repo
        elif repo == Settings.VEHICLES_CSV:
            return self.vehicles_on_premises_repo
        elif repo == Settings.WHITELISTED_CSV:
            return self.whitelisted_vehicles_repo
        elif repo == Settings.USERS_CSV:
            return self.users_repo
        else:
            raise ValueError(f"Invalid repository specified.{repo}")

    # def get_data(self, query, repo):
    #     """Retrieve data from the specified repository."""
    #     if repo == 'granted':
    #         return self.access_granted_repo.get(query)
    #     elif repo == 'denied':
    #         return self.access_denied_repo.get(query)
    #     elif repo == 'vehicles':
    #         return self.vehicles_on_premises_repo.get_all()
    #     elif repo == 'whitelisted':
    #         return self.whitelisted_vehicles_repo.get(query)
    #     else:
    #         raise ValueError("Invalid repository specified.")

    def get_data(self, repo, filters=None):
        """Retrieve data from the specified repository."""
        if repo == 'granted':
            return self.access_granted_repo.get(filters)
        elif repo == 'denied':
            return self.access_denied_repo.get(filters)
        elif repo == 'vehicles':
            return self.vehicles_on_premises_repo.get_all()
        elif repo == 'whitelisted':
            return self.whitelisted_vehicles_repo.get(filters)
        else:
            raise ValueError("Invalid repository specified.")

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
