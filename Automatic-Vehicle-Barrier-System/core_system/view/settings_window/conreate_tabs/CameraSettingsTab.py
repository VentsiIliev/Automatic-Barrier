from PyQt5.QtWidgets import QLineEdit, QComboBox

from core_system.view.settings_window.BaseTab import BaseTab
from core_system.config.settings.concreate_settings.CameraSettings import CameraSettings


class CameraTab(BaseTab):
    def __init__(self, settings_manager, camera_controller):
        super().__init__()
        self.settings_manager = settings_manager
        self.camera_controller = camera_controller
        # self.settings = settings_manager.get_camera_settings()
        self.camera_index_input = QLineEdit()
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["640x480", "1280x720", "1920x1080"])

        # Add form fields
        self.add_form_row("Camera Index:", self.camera_index_input)
        self.add_form_row("Resolution:", self.resolution_combo)
        self.set_values()
        self.add_save_button()

    def set_values(self):
        """Set values for the form fields."""
        # Set the default value for the camera index (for example, 1)
        self.camera_index_input.setText(str(self.settings_manager.get_camera_index()))

        # Set the default resolution (for example, "1280x720")
        resolution = f"{self.settings_manager.get_camera_width()}x{self.settings_manager.get_camera_height()}"
        print("resolution", resolution)
        index = self.resolution_combo.findText(resolution)
        if index != -1:
            self.resolution_combo.setCurrentIndex(index)

    def save_settings(self):
        camera_index = self.camera_index_input.text()
        resolution = self.resolution_combo.currentText()

        self.settings_manager.set_camera_index(int(camera_index))
        width, height = resolution.split("x")
        self.settings_manager.set_camera_width(int(width))
        self.settings_manager.set_camera_height(int(height))

        new_camera_settings = CameraSettings()
        new_camera_settings.set_camera_index(int(camera_index))
        new_camera_settings.set_resolution(int(width), int(height))
        new_camera_settings.set_width(int(width))
        new_camera_settings.set_height(int(height))

        self.settings_manager.save_settings_to_json(new_camera_settings)
        self.camera_controller.restart_camera(new_camera_settings)
        print(f"Saved Camera Settings: Index - {camera_index}, Resolution - {resolution}")
