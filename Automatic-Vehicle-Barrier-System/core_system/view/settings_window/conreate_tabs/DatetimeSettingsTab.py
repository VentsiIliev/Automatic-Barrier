from PyQt5.QtWidgets import QComboBox, QLabel, QHBoxLayout

from core_system.config.settings.concreate_settings.DateTimeSettings import DateTimeSettings
from core_system.view.settings_window.BaseTab import BaseTab


# DateTime settings Tab
class DateTimeTab(BaseTab):
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager

        # Date format dropdown
        self.date_format_combo = QComboBox()
        self.date_format_combo.addItems(["YYYY-MM-DD", "DD/MM/YYYY", "MM-DD-YYYY"])
        self.add_form_row("Date Format:", self.date_format_combo)

        # Time format dropdown
        self.time_format_combo = QComboBox()
        self.time_format_combo.addItems(["HH:MM:SS", "hh:MM AM/PM"])
        self.add_form_row("Time Format:", self.time_format_combo)
        # self.set_values()
        self.add_save_button()

    def save_settings(self):
        date_format = self.date_format_combo.currentText()
        time_format = self.time_format_combo.currentText()

        new_settings = DateTimeSettings()
        new_settings.set_date_format(date_format)
        new_settings.set_time_format(time_format)

        self.settings_manager.save_settings_to_json(new_settings)
