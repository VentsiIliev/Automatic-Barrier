# Database settings Tab
from PyQt5.QtWidgets import QLineEdit

from core_system.view.settings_window.BaseTab import BaseTab


class DatabaseTab(BaseTab):
    def __init__(self,settings_manager):
        super().__init__()
        # self.settings = settings_manager.get_database_settings()
        # Database connection input
        self.db_connection_input = QLineEdit()
        self.add_form_row("Database Connection String:", self.db_connection_input)
        self.add_save_button()

    def save_settings(self):
        db_connection = self.db_connection_input.text()
        self.settings_manager.save_settings_to_json(self.settings)
        print(f"Saved Database Settings: Connection - {db_connection}")