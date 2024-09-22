import json
import os

from core_system.config.CameraSetting import CameraSetting
from core_system.config.Settings import Settings
from core_system.config.SystemSetting import SystemSetting


class SettingsManger:
    def __init__(self):

        self.system_settings = {
            SystemSetting.ENFORCE_ACCESS_CONTROL.value: "False",
            SystemSetting.WORKDAY_START_TIME.value: "08:00",
            SystemSetting.WORKDAY_END_TIME.value: "17:00"
        }
        self.camera_settings = {
            CameraSetting.INDEX.value: 1,
            CameraSetting.WIDTH.value: 1280,
            CameraSetting.HEIGHT.value: 720
        }
        self.settings_file_paths = {
            "system_settings": 'core_system/config/system_settings.json',
            "camera_settings": "core_system/config/camera_settings.json"
        }

        self.load_all_settings()

    def load_all_settings(self):
        """Load settings from all specified JSON files."""
        for key, file_path in self.settings_file_paths.items():
            if os.path.exists(file_path):
                self.load_settings(file_path, key)
            else:
                print(f"File {file_path} not found. Using default settings for {key}.")
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
                    print(f"Unknown settings type '{key}'.")



        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the file {file_path}.")
        except Exception as e:
            print(f"An error occurred while loading settings from {file_path}: {e}")

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
            print(f"An error occurred while saving settings: {e}")

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
