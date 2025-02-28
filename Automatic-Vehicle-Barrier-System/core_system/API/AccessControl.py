import csv
from datetime import datetime

from shared.CSVFileName import CSVFileName
from shared.SingletonDatabase import SingletonDatabase
from core_system.model.access_events.AccessLevel import AccessLevel


class AccessControl:
    def __init__(self,  working_hours: str):
        # Load whitelisted vehicles and their access levels from the CSV file
        # self.whitelisted_vehicles = self.load_whitelisted_vehicles(csv_file)

        self.working_hours = working_hours

    def load_whitelisted_vehicles(self, csv_file):
        """Load the whitelisted vehicles and their access levels from a CSV file."""
        whitelisted_vehicles = {}
        try:
            with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
                # Specify the delimiter as ';' if your CSV uses semicolons
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    # Print debugging information
                    print(f"Row keys: {row.keys()}")
                    print(f"Row values: {row}")

                    # Access the columns using exact names
                    license_plate = row.get('License Plate')
                    access_level_str = row.get('Access Level')

                    if license_plate is None or access_level_str is None:
                        print(f"Missing expected column in row: {row}")
                        continue

                    # Convert the access level from string to AccessLevel enum
                    try:
                        access_level = AccessLevel(int(access_level_str))
                    except ValueError:
                        print(f"Invalid access level '{access_level_str}' in CSV.")
                        continue

                    whitelisted_vehicles[license_plate] = access_level
        except FileNotFoundError:
            print(f"File {csv_file} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return whitelisted_vehicles

    def check_access(self, registration_number):
        """Check if the registration number and access level are in the whitelist."""
        vehicles = SingletonDatabase().getInstance().get_repo(CSVFileName.WHITELISTED_VEHICLES.strip_extension()).get_all()
        vechicle = None
        for entry in vehicles:
            if entry.registration_number == registration_number:
                vechicle = entry
        if not vechicle:
            print(f"Vehicle with registration number '{registration_number}' is not whitelisted.")
            return False

        vehicle_access_level = vechicle.access_level
        print(f"Vehicle with registration number '{registration_number}' has access level '{vehicle_access_level}'.")

        if vehicle_access_level == AccessLevel.UNLIMITED:
            return True

        if vehicle_access_level == AccessLevel.WORKHOURS:
            # Check if the current time is within working hours (9 AM to 5 PM)
            current_time = datetime.now().time()
            start_time_str, end_time_str = self.working_hours.split('-')
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            return start_time <= current_time <= end_time
        raise ValueError(
            f"Invalid access level '{vehicle_access_level}' for vehicle with registration number '{registration_number}'.")
