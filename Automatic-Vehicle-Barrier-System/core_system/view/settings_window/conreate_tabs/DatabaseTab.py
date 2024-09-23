# Database Settings Tab
from PyQt5.QtWidgets import QLineEdit

from core_system.view.settings_window.BaseTab import BaseTab


class DatabaseTab(BaseTab):
    def __init__(self):
        super().__init__()

        # Database connection input
        self.db_connection_input = QLineEdit()
        self.add_form_row("Database Connection String:", self.db_connection_input)
        self.add_save_button()