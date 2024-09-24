import json

class DateTimeSettings:
    def __init__(self, date_format="yyyy-MM-dd", time_format="HH:mm:ss"):
        """Initialize with default date and time format or load from file."""
        self.date_format = date_format
        self.time_format = time_format

    def set_date_format(self, date_format):
        """Set the date format."""
        self.date_format = date_format

    def set_time_format(self, time_format):
        """Set the time format."""
        self.time_format = time_format

    def load_settings(self, filename="datetime_settings.json"):
        """Load settings from a JSON file."""
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.date_format = data.get("date_format", self.date_format)
                self.time_format = data.get("time_format", self.time_format)
        except FileNotFoundError:
            print(f"{filename} not found, using default settings.")
        except json.JSONDecodeError:
            print(f"Error decoding {filename}, using default settings.")

    def save_settings(self, filename="datetime_settings.json"):
        """Save the current settings to a JSON file."""
        settings_data = {
            "date_format": self.date_format,
            "time_format": self.time_format
        }
        with open(filename, "w") as file:
            json.dump(settings_data, file, indent=4)

    def __repr__(self):
        return f"DateTimeSettings(date_format='{self.date_format}', time_format='{self.time_format}')"
