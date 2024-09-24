from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QTimeEdit, QCheckBox

from core_system.view.settings_window.BaseTab import BaseTab
from core_system.config.settings.concreate_settings.AccessControlSettings import AccessControlSettings


# Access Control Tab
class AccessControlTab(BaseTab):
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        # self.settings = self.settings_manager.get_access_control_settings()
        self.date_time_settings = self.settings_manager.get_date_format()
        self.time_format = self.settings_manager.get_time_format()
        # Load access control settings
        self.access_control_settings = AccessControlSettings()

        # Enforce access control checkbox
        self.enforce_access_control_checkbox = QCheckBox("Enforce Access Control")
        self.enforce_access_control_checkbox.setStyleSheet("font-weight: bold;")
        self.enforce_access_control_checkbox.setChecked(self.access_control_settings.enforce_access_control)
        self.layout.addWidget(self.enforce_access_control_checkbox)

        # Workday start time input
        self.workday_start_time_input = QTimeEdit()
        start_time = QTime.fromString(self.access_control_settings.get_workday_start_time(), self.time_format)
        self.workday_start_time_input.setTime(start_time)
        self.add_form_row("Start Time:", self.workday_start_time_input)

        # Workday end time input
        self.workday_end_time_input = QTimeEdit()
        end_time = QTime.fromString(self.access_control_settings.get_workday_end_time(), self.time_format)
        self.workday_end_time_input.setTime(end_time)
        self.add_form_row("End Time:", self.workday_end_time_input)

        # self.set_values()
        # Add save button to handle saving the settings
        self.add_save_button()

    def set_values(self):
        """Set values for the form fields."""
        # Set the default value for the enforce access control checkbox
        self.enforce_access_control_checkbox.setChecked(self.access_control_settings.enforce_access_control)

        # Set the default workday start time
        start_time = QTime.fromString(self.access_control_settings.workday_start_time, self.time_format)
        self.workday_start_time_input.setTime(start_time)

        # Set the default workday end time
        end_time = QTime.fromString(self.access_control_settings.workday_end_time, self.time_format)
        self.workday_end_time_input.setTime(end_time)

    def save_settings(self):
        # get values from the widgets
        enforce_access_control = self.enforce_access_control_checkbox.isChecked()
        workday_start_time = self.workday_start_time_input.time().toString(self.time_format)
        workday_end_time = self.workday_end_time_input.time().toString(self.time_format)

        """Saves the settings from the tab back to AccessControlSettings."""
        self.settings_manager.set_enforce_access_control(enforce_access_control)
        self.settings_manager.set_workday_start_time(workday_start_time)
        self.settings_manager.set_workday_end_time(workday_end_time)

        new_settings = AccessControlSettings()
        new_settings.set_enforce_access_control(enforce_access_control)
        new_settings.set_workday_start_time(workday_start_time)
        new_settings.set_workday_end_time(workday_end_time)

        self.settings_manager.save_settings_to_json(new_settings)
        # show confirmation
        print("Settings Saved!")



