from PyQt5.QtWidgets import QComboBox, QLabel, QHBoxLayout

from core_system.view.settings_window.BaseTab import BaseTab


# DateTime Settings Tab
class DateTimeTab(BaseTab):
    def __init__(self):
        super().__init__()

        # Date format dropdown
        self.date_format_combo = QComboBox()
        self.date_format_combo.addItems(["YYYY-MM-DD", "DD/MM/YYYY", "MM-DD-YYYY"])
        self.add_form_row("Date Format:", self.date_format_combo)

        # Time format dropdown
        self.time_format_combo = QComboBox()
        self.time_format_combo.addItems(["HH:MM:SS", "hh:MM AM/PM"])
        self.add_form_row("Time Format:", self.time_format_combo)
        self.add_save_button()