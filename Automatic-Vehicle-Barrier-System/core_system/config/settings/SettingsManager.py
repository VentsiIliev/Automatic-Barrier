import json
import os
from core_system.config.settings.concreate_settings.AccessControlSettings import AccessControlSettings
from core_system.config.settings.concreate_settings.CameraSettings import CameraSettings
from core_system.config.settings.concreate_settings.DateTimeSettings import DateTimeSettings


class SettingsManager:
    settings_dir = os.path.join("core_system", "assets", "settings")
    settings_file_paths = {
        "camera": os.path.join(settings_dir, "camera_settings.json"),
        "access_control": os.path.join(settings_dir, "access_control_settings.json"),
        "date_time": os.path.join(settings_dir, "date_time_settings.json")
    }

    def __init__(self):
        # Initialize a dictionary to store settings objects
        self.settings_objects = {}

        # Initialize and load settings for each component
        self.camera_settings = CameraSettings()
        self.access_control_settings = AccessControlSettings()
        self.date_time_settings = DateTimeSettings()

        # Store them in the settings dictionary
        self.settings_objects["camera"] = self.camera_settings
        self.settings_objects["access_control"] = self.access_control_settings
        self.settings_objects["date_time"] = self.date_time_settings

        # Load settings from JSON files, or use default values if files do not exist
        self.load_all_settings()

    def set_enforce_access_control(self, value):
        self.access_control_settings.set_enforce_access_control(value)

    def set_workday_start_time(self, time):
        self.access_control_settings.set_workday_start_time(time)

    def set_workday_end_time(self, time):
        self.access_control_settings.set_workday_end_time(time)

    def set_camera_index(self, index):
        self.camera_settings.set_camera_index(index)

    def set_camera_width(self, width):
        self.camera_settings.set_width(width)

    def set_camera_height(self, height):
        self.camera_settings.set_height(height)

    def get_camera_index(self):
        return self.camera_settings.get_camera_index()

    def get_camera_width(self):
        return self.camera_settings.get_camera_width()

    def get_camera_height(self):
        return self.camera_settings.get_camera_height()

    def get_enforce_access_control(self):
        return self.access_control_settings.get_enforce_access_control()

    def get_workday_start_time(self):
        return self.access_control_settings.get_workday_start_time()

    def get_workday_end_time(self):
        return self.access_control_settings.get_workday_end_time()

    def get_date_format(self):
        return self.date_time_settings.get_date_format()

    def get_time_format(self):
        return self.date_time_settings.get_time_format()

    def get_camera_settings(self):
        """Retrieve the camera settings object."""
        return self.camera_settings

    def get_access_control_settings(self):
        """Retrieve the access control settings object."""
        return self.access_control_settings

    def get_date_time_settings(self):
        """Retrieve the date and time settings object."""
        return self.date_time_settings

    def get_settings(self, key):
        """Retrieve a settings object by key."""
        return self.settings_objects.get(key)

    def save_all_settings(self):
        """Save all settings to their respective files."""
        for key, settings_obj in self.settings_objects.items():
            filename = self.settings_file_paths.get(key)
            if filename:
                self.save_settings_to_json(filename, settings_obj)

    def load_all_settings(self):
        """Load all settings from their respective JSON files. Use default values if file doesn't exist."""
        for key, settings_obj in self.settings_objects.items():
            filename = self.settings_file_paths.get(key)
            if filename and os.path.exists(filename):
                self.load_settings_from_json(filename, settings_obj)
            else:
                print(f"{filename} not found. Using default values for {key} settings.")
                # Automatically save default settings to the missing file
                self.save_settings_to_json(filename, settings_obj)

    def display_all_settings(self):
        """Utility function to display all settings in the manager."""
        for key, settings_obj in self.settings_objects.items():
            print(f"Settings for {key}:")
            settings_obj.display_settings()
            print()

    def load_settings_from_json(self, json_file, settings_obj):
        """Load settings from a JSON file and update the settings object."""
        try:
            with open(json_file, 'r') as f:
                settings_data = json.load(f)

            if isinstance(settings_obj, CameraSettings):
                settings_obj.set_camera_index(settings_data.get("index", 1))
                settings_obj.set_resolution(settings_data.get("width", 1280), settings_data.get("height", 720))

            elif isinstance(settings_obj, AccessControlSettings):
                settings_obj.set_enforce_access_control(settings_data.get("enforce_access_control", False))
                settings_obj.set_workday_start_time(settings_data.get("workday_start_time", "08:00"))
                settings_obj.set_workday_end_time(settings_data.get("workday_end_time", "17:00"))

            elif isinstance(settings_obj, DateTimeSettings):
                settings_obj.set_date_format(settings_data.get("date_format", "yyyy-MM-dd"))
                settings_obj.set_time_format(settings_data.get("time_format", "HH:mm:ss"))

            print(f"Settings loaded from {json_file}.")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading settings from {json_file}: {e}")
            print(f"Using default values for {type(settings_obj).__name__}.")

    def save_settings_to_json(self, settings_obj):
        """Save the settings object to a JSON file."""
        try:
            # Create the settings directory if it doesn't exist
            os.makedirs(self.settings_dir, exist_ok=True)

            settings_data = {}
            if isinstance(settings_obj, CameraSettings):
                json_file = self.settings_file_paths.get("camera")
                settings_data = {
                    "index": settings_obj.get_camera_index(),
                    "width": settings_obj.get_camera_width(),
                    "height": settings_obj.get_camera_height()
                }

            elif isinstance(settings_obj, AccessControlSettings):
                json_file = self.settings_file_paths.get("access_control")
                settings_data = {
                    "enforce_access_control": settings_obj.get_enforce_access_control(),
                    "workday_start_time": settings_obj.get_workday_start_time(),
                    "workday_end_time": settings_obj.get_workday_end_time()
                }

            elif isinstance(settings_obj, DateTimeSettings):
                json_file = self.settings_file_paths.get("date_time")
                settings_data = {
                    "date_format": settings_obj.get_date_format(),
                    "time_format": settings_obj.get_time_format()
                }

            # Write settings data to the JSON file
            with open(json_file, 'w') as f:
                json.dump(settings_data, f, indent=4)

            print(f"Settings saved to {json_file}.")

        except Exception as e:
            print(f"Error saving settings to {json_file}: {e}")
