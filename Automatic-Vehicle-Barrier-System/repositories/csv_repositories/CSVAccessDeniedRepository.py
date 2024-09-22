from model.access_events.AccessEvent import AccessEvent
from repositories.csv_repositories.BaseCSVRepository import BaseCSVRepository
from repositories.csv_repositories.Constants import ACCESS_DENIED_FIELDS, EVENT_TYPE, DATE, TIME, REGISTRATION_NUMBER, DIRECTION, OWNER

class CSVAccessDeniedRepository(BaseCSVRepository):
    def __init__(self, file_path):
        super().__init__(file_path, ACCESS_DENIED_FIELDS)

    def get_all(self):
        """Retrieve all access denial events from the repository."""
        df = self._read_rows()
        return [
            AccessEvent(
                row[EVENT_TYPE],
                row[DATE],
                row[TIME],
                row[REGISTRATION_NUMBER],
                row[DIRECTION]
            )
            for index, row in df.iterrows()
        ]

    def insert(self, event_type, date, time, registration_number, direction, owner):
        """Insert a new access denial event into the repository."""
        super().insert(**{
            EVENT_TYPE: event_type,
            DATE: date,
            TIME: time,
            REGISTRATION_NUMBER: registration_number,
            DIRECTION: direction,
            OWNER: owner
        })

    def get(self, registration_number):
        """Retrieve an event by registration number."""
        df = self._read_rows()
        event_row = df[df[REGISTRATION_NUMBER] == registration_number]
        if not event_row.empty:
            return AccessEvent(
                event_row.iloc[0][EVENT_TYPE],
                event_row.iloc[0][DATE],
                event_row.iloc[0][TIME],
                event_row.iloc[0][REGISTRATION_NUMBER],
                event_row.iloc[0][DIRECTION]
            )
        return None

    def get_data(self, filters=None):
        """Retrieve filtered data based on given criteria."""
        return super().get_data(filters)