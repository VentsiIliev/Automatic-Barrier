from PyQt5.QtWidgets import QHBoxLayout, QLabel, QComboBox

from core_system.view.settings_window.BaseTab import BaseTab


# System Settings Tab
class SystemTab(BaseTab):
    def __init__(self):
        super().__init__()

        # Theme dropdown
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.add_form_row("Theme:", self.theme_combo)
        self.add_save_button()
