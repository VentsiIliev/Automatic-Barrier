class AccessControlSettings:
    def __init__(self):
        # Initialize default settings values
        self.enforce_access_control = False
        self.workday_start_time = "08:00"
        self.workday_end_time = "17:00"

    def set_enforce_access_control(self, value: bool):
        """Set whether access control is enforced."""
        self.enforce_access_control = value

    def set_workday_start_time(self, time: str):
        """Set the workday start time (format: HH:MM)."""
        self.workday_start_time = time

    def set_workday_end_time(self, time: str):
        """Set the workday end time (format: HH:MM)."""
        self.workday_end_time = time

    def get_settings(self):
        """Get the current settings as a dictionary."""
        return {
            "enforce access control": self.enforce_access_control,
            "workday start time": self.workday_start_time,
            "workday end time": self.workday_end_time
        }

    def load_settings(self, filename: str):
        """Load settings from a file."""
        try:
            with open(filename, 'r') as file:
                data = eval(file.read())
                self.enforce_access_control = data.get("enforce_access_control", False)
                self.workday_start_time = data.get("workday_start_time", "08:00")
                self.workday_end_time = data.get("workday_end_time", "17:00")
        except FileNotFoundError:
            print(f"{filename} not found. Using default settings.")

    def save_settings(self, filename: str):
        """Save the current settings to a file."""
        with open(filename, 'w') as file:
            file.write(str(self.get_settings()))

    def display_settings(self):
        """Print the current settings."""
        print(f"Enforce Access Control: {self.enforce_access_control}")
        print(f"Workday Start Time: {self.workday_start_time}")
        print(f"Workday End Time: {self.workday_end_time}")

    def get_enforce_access_control(self):
        return self.enforce_access_control

    def get_workday_start_time(self):
        return self.workday_start_time

    def get_workday_end_time(self):
        return self.workday_end_time