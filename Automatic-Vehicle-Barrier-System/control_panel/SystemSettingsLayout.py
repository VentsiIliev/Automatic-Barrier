from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QTabWidget, QCheckBox

class SystemSettingsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        """Initialize the system settings layout with tabs."""
        layout = QVBoxLayout()

        # System Settings Title
        titleLabel = QLabel("System Settings", self)
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(titleLabel)

        # Create Tab Widget
        self.tabWidget = QTabWidget()

        # System Settings Tab
        self.systemSettingsTab = QWidget()
        self.setupSystemSettingsTab()
        self.tabWidget.addTab(self.systemSettingsTab, "System Settings")

        # Camera Settings Tab
        self.cameraSettingsTab = QWidget()
        self.setupCameraSettingsTab()
        self.tabWidget.addTab(self.cameraSettingsTab, "Camera Settings")

        layout.addWidget(self.tabWidget)
        self.setLayout(layout)

    def setupSystemSettingsTab(self):
        """Setup the UI for the System Settings tab."""
        layout = QVBoxLayout()

        # Enforce Access Control Checkbox
        self.enforceAccessControl = QCheckBox("Enforce Access Control", self)
        layout.addWidget(self.enforceAccessControl)

        # Working Hours Section
        workingHoursLayout = QHBoxLayout()
        workingHoursLabel = QLabel("Working Hours:", self)
        self.workingHoursInput = QLineEdit(self)
        self.workingHoursInput.setPlaceholderText("Enter hours (e.g., 08:00-17:00)")

        workingHoursLayout.addWidget(workingHoursLabel)
        workingHoursLayout.addWidget(self.workingHoursInput)

        layout.addLayout(workingHoursLayout)

        # Workday Start Time Section
        workdayStartLayout = QHBoxLayout()
        workdayStartLabel = QLabel("Workday Start Time:", self)
        self.workdayStartInput = QLineEdit(self)
        self.workdayStartInput.setPlaceholderText("Enter start time (e.g., 08:00)")

        workdayStartLayout.addWidget(workdayStartLabel)
        workdayStartLayout.addWidget(self.workdayStartInput)

        layout.addLayout(workdayStartLayout)

        # Workday End Time Section
        workdayEndLayout = QHBoxLayout()
        workdayEndLabel = QLabel("Workday End Time:", self)
        self.workdayEndInput = QLineEdit(self)
        self.workdayEndInput.setPlaceholderText("Enter end time (e.g., 17:00)")

        workdayEndLayout.addWidget(workdayEndLabel)
        workdayEndLayout.addWidget(self.workdayEndInput)

        layout.addLayout(workdayEndLayout)

        # Save Settings Button
        saveButton = QPushButton("Save Settings", self)
        saveButton.clicked.connect(self.saveSettings)
        layout.addWidget(saveButton)

        # Finalize System Settings Tab Layout
        self.systemSettingsTab.setLayout(layout)

    def setupCameraSettingsTab(self):
        """Setup the UI for the Camera Settings tab."""
        layout = QVBoxLayout()

        # Camera Settings
        cameraLabel = QLabel("Camera Settings", self)
        cameraLabel.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(cameraLabel)

        # Camera Index Section
        cameraIndexLayout = QHBoxLayout()
        cameraIndexLabel = QLabel("Camera Index:", self)
        self.cameraIndexInput = QLineEdit(self)
        self.cameraIndexInput.setPlaceholderText("Enter camera index (e.g., 1)")

        cameraIndexLayout.addWidget(cameraIndexLabel)
        cameraIndexLayout.addWidget(self.cameraIndexInput)

        layout.addLayout(cameraIndexLayout)

        # Camera Width Section
        cameraWidthLayout = QHBoxLayout()
        cameraWidthLabel = QLabel("Camera Width:", self)
        self.cameraWidthInput = QLineEdit(self)
        self.cameraWidthInput.setPlaceholderText("Enter width (e.g., 1280)")

        cameraWidthLayout.addWidget(cameraWidthLabel)
        cameraWidthLayout.addWidget(self.cameraWidthInput)

        layout.addLayout(cameraWidthLayout)

        # Camera Height Section
        cameraHeightLayout = QHBoxLayout()
        cameraHeightLabel = QLabel("Camera Height:", self)
        self.cameraHeightInput = QLineEdit(self)
        self.cameraHeightInput.setPlaceholderText("Enter height (e.g., 720)")

        cameraHeightLayout.addWidget(cameraHeightLabel)
        cameraHeightLayout.addWidget(self.cameraHeightInput)

        layout.addLayout(cameraHeightLayout)

        # Brightness Control Checkbox
        self.brightnessControl = QCheckBox("Enable Brightness Control", self)
        layout.addWidget(self.brightnessControl)

        # Save Camera Settings Button
        saveCameraButton = QPushButton("Save Camera Settings", self)
        saveCameraButton.clicked.connect(self.saveCameraSettings)
        layout.addWidget(saveCameraButton)

        # Finalize Camera Settings Tab Layout
        self.cameraSettingsTab.setLayout(layout)

    def saveSettings(self):
        """Save system settings including access control and hours."""
        enforce_access = self.enforceAccessControl.isChecked()
        working_hours = self.workingHoursInput.text()
        workday_start = self.workdayStartInput.text()
        workday_end = self.workdayEndInput.text()

        # For now, show a message box with the settings
        settings_message = (
            f"Settings Saved:\n"
            f"Enforce Access Control: {'Enabled' if enforce_access else 'Disabled'}\n"
            f"Working Hours: {working_hours}\n"
            f"Workday Start Time: {workday_start}\n"
            f"Workday End Time: {workday_end}"
        )
        QMessageBox.information(self, "Settings Saved", settings_message)

        # Clear input fields
        self.workingHoursInput.clear()
        self.workdayStartInput.clear()
        self.workdayEndInput.clear()

    def saveCameraSettings(self):
        """Save camera settings including index, width, height, and brightness control."""
        camera_index = self.cameraIndexInput.text()
        camera_width = self.cameraWidthInput.text()
        camera_height = self.cameraHeightInput.text()
        brightness_control = self.brightnessControl.isChecked()

        # For now, show a message box with the camera settings
        camera_settings_message = (
            f"Camera Settings Saved:\n"
            f"Index: {camera_index}\n"
            f"Width: {camera_width}\n"
            f"Height: {camera_height}\n"
            f"Brightness Control: {'Enabled' if brightness_control else 'Disabled'}"
        )
        QMessageBox.information(self, "Camera Settings Saved", camera_settings_message)

        # Clear input fields
        self.cameraIndexInput.clear()
        self.cameraWidthInput.clear()
        self.cameraHeightInput.clear()

    def saveCameraUrl(self):
        """Save the camera URL."""
        camera_url = self.cameraUrlInput.text()
        if camera_url:
            QMessageBox.information(self, "Success", f"Camera URL set to: {camera_url}")
            self.cameraUrlInput.clear()
        else:
            QMessageBox.warning(self, "Error", "Please enter a valid camera URL.")
