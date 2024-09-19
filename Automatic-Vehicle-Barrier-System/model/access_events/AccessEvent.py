class AccessEvent:
    def __init__(self, event_type, event_time, registration_number):
        self.type = event_type
        self.time = event_time
        self.registration_number = registration_number

    def __str__(self):
        return f"{self.type.value} at {self.time} from {self.registration_number}"