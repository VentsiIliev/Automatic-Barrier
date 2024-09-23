from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QTimeEdit, QLineEdit, QCheckBox

from core_system.view.settings_window.BaseTab import BaseTab


# Access Control Tab
class AccessControlTab(BaseTab):
    def __init__(self):
        super().__init__()

        # Enforce access control checkbox
        self.enforce_access_control_checkbox = QCheckBox("Enforce Access Control")
        self.enforce_access_control_checkbox.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.enforce_access_control_checkbox)

        # Working hours input
        self.working_hours_input = QLineEdit("08:00-17:00")
        self.add_form_row("Working Hours:", self.working_hours_input)

        # Start Time
        self.workday_start_time_input = QTimeEdit()
        self.add_form_row("Start Time:", self.workday_start_time_input)

        # End Time
        self.workday_end_time_input = QTimeEdit()
        self.add_form_row("End Time:", self.workday_end_time_input)

        self.add_save_button()