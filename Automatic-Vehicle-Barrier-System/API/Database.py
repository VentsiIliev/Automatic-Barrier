import os

from model.access_events.AccessEventType import AccessEventType


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.access_denied_table = "database/access_denied.csv"
        self.access_granted_table = "database/access_granted.csv"

    def get_data(self, query):
        # Connect to the database and get the data
        pass

    def insert_data(self, query):
        # Connect to the database and insert the data
        pass

    def delete_data(self, query):
        # Connect to the database and delete the data
        pass

    def update_data(self, query):
        # Connect to the database and update the data
        pass

    def log_access_granted(self, event):
        # Prepare the string for the CSV row
        event_type = event.type.value
        event_time = event.time.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime for CSV
        registration_number = event.registration_number
        direction = event.direction
        row = f"{event_type},{event_time},{registration_number},{direction}\n"

        # Check if the file exists and create it with the header if necessary
        if not os.path.exists(self.access_granted_table):
            with open(self.access_granted_table, 'w') as f:
                # Write the header
                f.write("Event Type,Date Time,Registration Number\n")

        # Append the event details to the file
        with open(self.access_granted_table, 'a') as f:
            f.write(row)

    def log_access_denied(self, event):
        # Prepare the string for the CSV row
        event_type = event.type.value
        event_time = event.time.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime for CSV
        registration_number = event.registration_number
        direction = event.direction
        row = f"{event_type},{event_time},{registration_number},{direction}\n"

        # Check if the file exists and create it with the header if necessary
        if not os.path.exists(self.access_denied_table):
            with open(self.access_denied_table, 'w') as f:
                # Write the header
                f.write("Event Type,Date Time,Registration Number\n")

        # Append the event details to the file
        with open(self.access_denied_table, 'a') as f:
            f.write(row)

    def log_event(self, event):
        if event.type == AccessEventType.GRANTED:
            self.log_access_granted(event)
        elif event.type == AccessEventType.DENIED:
            self.log_access_denied(event)
        else:
            raise ValueError("Invalid event type")
