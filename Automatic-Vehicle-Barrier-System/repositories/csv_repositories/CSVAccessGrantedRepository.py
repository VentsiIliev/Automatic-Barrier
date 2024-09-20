from repositories.csv_repositories.Constants import ACCESS_GRANTED_FIELDS, EVENT_TYPE, DATE, TIME, REGISTRATION_NUMBER, \
    DIRECTION, OWNER
from repositories.csv_repositories.BaseCSVRepository import BaseCSVRepository


class CSVAccessGrantedRepository(BaseCSVRepository):
    def __init__(self, file_path):
        super().__init__(file_path, ACCESS_GRANTED_FIELDS)

    def insert(self, event_type, date, time, registration_number, direction, owner):
        super().insert(**{
            EVENT_TYPE: event_type,
            DATE: date,
            TIME: time,
            REGISTRATION_NUMBER: registration_number,
            DIRECTION: direction,
            OWNER: owner
        })

    def get(self, registration_number):
        return super().get(registration_number)
