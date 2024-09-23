from PyQt5.QtWidgets import QLineEdit, QComboBox

from core_system.view.settings_window.BaseTab import BaseTab


class CameraTab(BaseTab):
    def __init__(self):
        super().__init__()
        self.camera_index_input = QLineEdit()
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["640x480", "1280x720", "1920x1080"])

        # Add form fields
        self.add_form_row("Camera Index:", self.camera_index_input)
        self.add_form_row("Resolution:", self.resolution_combo)
        self.add_save_button()

    def save_settings(self):
        camera_index = self.camera_index_input.text()
        resolution = self.resolution_combo.currentText()
        print(f"Saved Camera Settings: Index - {camera_index}, Resolution - {resolution}")
