class AccessControl:
    def __init__(self):
        self.whitelisted_vehicles = ["X0640KC"]

    def check_access(self, registration_number):
        return registration_number in self.whitelisted_vehicles
