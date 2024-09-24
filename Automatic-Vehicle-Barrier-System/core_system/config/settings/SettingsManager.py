from core_system.config.settings.concreate_settings.AccessControlSettings import AccessControlSettings
from core_system.config.settings.concreate_settings.CameraSettings import CameraSettings
from core_system.config.settings.concreate_settings.DateTimeSettings import DateTimeSettings


class SettingsManager:
    def __init__(self):
        # Initialize a dictionary to store settings objects
        self.settings_objects = {}

        # Add CameraSettings to the manager
        self.camera_settings = CameraSettings()
        self.access_control_settings = AccessControlSettings()
        self.date_time_settings = DateTimeSettings()

        self.settings_objects["camera"] = self.camera_settings

    def get_settings(self, key):
        """Retrieve a settings object by key."""
        return self.settings_objects.get(key)

    def add_settings(self, key, settings_obj):
        """Add a new settings object to the manager."""
        self.settings_objects[key] = settings_obj

    def save_all_settings(self):
        """Save all settings to their respective files."""
        for key, settings_obj in self.settings_objects.items():
            filename = f"{key}_settings.txt"
            settings_obj.save_settings(filename)

    def load_all_settings(self):
        """Load all settings from their respective files."""
        for key, settings_obj in self.settings_objects.items():
            filename = f"{key}_settings.txt"
            settings_obj.load_settings(filename)

    def display_all_settings(self):
        """Utility function to display all settings in the manager."""
        for key, settings_obj in self.settings_objects.items():
            print(f"Settings for {key}:")
            settings_obj.display_settings()
            print()
