from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QTimeEdit, QCheckBox

from core_system.view.settings_window.BaseTab import BaseTab
from core_system.config.settings.concreate_settings.AccessControlSettings import AccessControlSettings


# Access Control Tab
class AccessControlTab(BaseTab):
    def __init__(self):
        super().__init__()

        # Load access control settings
        self.access_control_settings = AccessControlSettings()

        # Enforce access control checkbox
        self.enforce_access_control_checkbox = QCheckBox("Enforce Access Control")
        self.enforce_access_control_checkbox.setStyleSheet("font-weight: bold;")
        self.enforce_access_control_checkbox.setChecked(self.access_control_settings.enforce_access_control)
        self.layout.addWidget(self.enforce_access_control_checkbox)

        # Workday start time input
        self.workday_start_time_input = QTimeEdit()
        start_time = QTime.fromString(self.access_control_settings.workday_start_time, "HH:mm")
        self.workday_start_time_input.setTime(start_time)
        self.add_form_row("Start Time:", self.workday_start_time_input)

        # Workday end time input
        self.workday_end_time_input = QTimeEdit()
        end_time = QTime.fromString(self.access_control_settings.workday_end_time, "HH:mm")
        self.workday_end_time_input.setTime(end_time)
        self.add_form_row("End Time:", self.workday_end_time_input)

        # Add save button to handle saving the settings
        self.add_save_button()

    def save_settings(self):
        """Saves the settings from the tab back to AccessControlSettings."""
        # Update settings from user input
        self.access_control_settings.set_enforce_access_control(self.enforce_access_control_checkbox.isChecked())
        self.access_control_settings.set_workday_start_time(self.workday_start_time_input.time().toString("HH:mm"))
        self.access_control_settings.set_workday_end_time(self.workday_end_time_input.time().toString("HH:mm"))

        # Save settings to file (or any other storage)
        self.access_control_settings.save_settings("access_control_settings.txt")
        print("Access control settings saved!")
