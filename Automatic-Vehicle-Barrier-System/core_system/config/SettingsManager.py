import json
import os

from core_system.config.Settings import Settings
from core_system.config.SystemSetting import SystemSetting

# File paths
SYSTEM_SETTINGS_PATH = 'core_system/config/system_settings.json'
CAMERA_SETTINGS_PATH = 'core_system/config/camera_settings.json'

# Default system settings
DEFAULT_SYSTEM_SETTINGS = {
    "ENFORCE_ACCESS_CONTROL": "False",
    "WORKDAY_START_TIME": "08:00",
    "WORKDAY_END_TIME": "17:00"
}

# Default camera settings
DEFAULT_CAMERA_SETTINGS = {
    "INDEX": 1,
    "WIDTH": 1280,
    "HEIGHT": 720
}

# Error messages
FILE_NOT_FOUND_ERROR = "File {file_path} not found. Using default settings for {key}."
JSON_DECODE_ERROR = "Error decoding JSON from the file {file_path}."
GENERAL_LOAD_ERROR = "An error occurred while loading settings from {file_path}: {error}"
GENERAL_SAVE_ERROR = "An error occurred while saving settings: {error}"
UNKNOWN_SETTINGS_TYPE_ERROR = "Unknown settings type '{key}'."


class SettingsManager:
    def __init__(self):
        # Use constants for default settings
        self.system_settings = DEFAULT_SYSTEM_SETTINGS.copy()
        self.camera_settings = DEFAULT_CAMERA_SETTINGS.copy()

        # Use constants for file paths
        self.settings_file_paths = {
            "system_settings": SYSTEM_SETTINGS_PATH,
            "camera_settings": CAMERA_SETTINGS_PATH
        }

        self.load_all_settings()

    def load_all_settings(self):
        """Load settings from all specified JSON files."""
        for key, file_path in self.settings_file_paths.items():
            if os.path.exists(file_path):
                self.load_settings(file_path, key)
            else:
                # Use formatted error message from constants
                print(FILE_NOT_FOUND_ERROR.format(file_path=file_path, key=key))
        return Settings(self.system_settings, self.camera_settings)

    def load_settings(self, file_path: str, key: str):
        """Load settings from a specific JSON file and update the respective settings dictionary."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                loaded_settings = json.load(file)

                if key == "system_settings":
                    self.system_settings.update(loaded_settings)
                elif key == "camera_settings":
                    self.camera_settings.update(loaded_settings)
                else:
                    print(UNKNOWN_SETTINGS_TYPE_ERROR.format(key=key))

        except FileNotFoundError:
            print(FILE_NOT_FOUND_ERROR.format(file_path=file_path, key=key))
        except json.JSONDecodeError:
            print(JSON_DECODE_ERROR.format(file_path=file_path))
        except Exception as e:
            print(GENERAL_LOAD_ERROR.format(file_path=file_path, error=e))

    def save_settings(self):
        """Save all settings to their respective JSON files."""
        try:
            for key, file_path in self.settings_file_paths.items():
                if key == "system_settings":
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(self.system_settings, file, indent=4)
                elif key == "camera_settings":
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(self.camera_settings, file, indent=4)
        except Exception as e:
            print(GENERAL_SAVE_ERROR.format(error=e))

    def get_setting(self, setting: SystemSetting):
        """Get a specific setting."""
        return self.system_settings.get(setting.value)

    def set_setting(self, setting: SystemSetting, value):
        """Set a specific setting."""
        self.system_settings[setting.value] = value
        self.save_settings()

    def get_working_hours(self):
        """Get the working hours as a string."""
        workday_start_time = self.get_setting(SystemSetting.WORKDAY_START_TIME)
        workday_end_time = self.get_setting(SystemSetting.WORKDAY_END_TIME)
        return f"{workday_start_time}-{workday_end_time}"
