# SettingsWindow.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QTabWidget, QWidget, QCheckBox, QTimeEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QTime


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Setup the settings window
        self.setWindowTitle("settings")
        self.setStyleSheet("background-color: #f9f9f9; color: #4c4c4c;")
        self.setGeometry(200, 200, 400, 500)  # Adjust height for extra tabs

        layout = QVBoxLayout()

        # Header
        header = QLabel("settings")
        header.setFont(QFont("Arial", 22, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Create a tab widget
        self.tab_widget = QTabWidget()
        self.camera_settings_tab = self.create_camera_settings_tab()
        self.system_settings_tab = self.create_system_settings_tab()
        self.datetime_settings_tab = self.create_datetime_settings_tab()
        self.access_control_tab = self.create_access_control_tab()  # Add Access Control tab
        self.database_tab = self.create_database_tab()  # Add Database tab

        # Add tabs to the tab widget
        self.tab_widget.addTab(self.camera_settings_tab, "Camera settings")
        self.tab_widget.addTab(self.system_settings_tab, "System settings")
        self.tab_widget.addTab(self.datetime_settings_tab, "Date & Time settings")
        self.tab_widget.addTab(self.access_control_tab, "Access Control")
        self.tab_widget.addTab(self.database_tab, "Database settings")  # Add Database tab

        layout.addWidget(self.tab_widget)

        # Save and Cancel buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def create_camera_settings_tab(self):
        """Create the Camera settings tab"""
        camera_tab = QWidget()
        camera_layout = QVBoxLayout()

        # Camera Index
        camera_index_layout = QHBoxLayout()
        camera_index_label = QLabel("Camera Index:")
        self.camera_index_input = QLineEdit()
        camera_index_layout.addWidget(camera_index_label)
        camera_index_layout.addWidget(self.camera_index_input)
        camera_layout.addLayout(camera_index_layout)

        # Resolution
        resolution_layout = QHBoxLayout()
        resolution_label = QLabel("Resolution:")
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["640x480", "1280x720", "1920x1080"])
        resolution_layout.addWidget(resolution_label)
        resolution_layout.addWidget(self.resolution_combo)
        camera_layout.addLayout(resolution_layout)

        # Enable Brightness Control
        self.brightness_control_checkbox = QCheckBox("Enable Brightness Control")
        camera_layout.addWidget(self.brightness_control_checkbox)

        camera_tab.setLayout(camera_layout)
        return camera_tab

    def create_system_settings_tab(self):
        """Create the System settings tab"""
        system_tab = QWidget()
        system_layout = QVBoxLayout()

        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)

        system_layout.addLayout(theme_layout)

        # Add other system settings fields as needed...

        system_tab.setLayout(system_layout)
        return system_tab

    def create_datetime_settings_tab(self):
        """Create the Date & Time settings tab"""
        datetime_tab = QWidget()
        datetime_layout = QVBoxLayout()

        # Date Format
        date_format_layout = QHBoxLayout()
        date_format_label = QLabel("Date Format:")
        self.date_format_combo = QComboBox()
        self.date_format_combo.addItems(["YYYY-MM-DD", "DD/MM/YYYY", "MM-DD-YYYY"])
        date_format_layout.addWidget(date_format_label)
        date_format_layout.addWidget(self.date_format_combo)
        datetime_layout.addLayout(date_format_layout)

        # Time Format
        time_format_layout = QHBoxLayout()
        time_format_label = QLabel("Time Format:")
        self.time_format_combo = QComboBox()
        self.time_format_combo.addItems(["HH:MM:SS", "hh:MM AM/PM"])
        time_format_layout.addWidget(time_format_label)
        time_format_layout.addWidget(self.time_format_combo)
        datetime_layout.addLayout(time_format_layout)

        datetime_tab.setLayout(datetime_layout)
        return datetime_tab

    def create_access_control_tab(self):
        """Create the Access Control tab"""
        access_tab = QWidget()
        access_layout = QVBoxLayout()

        # Enforce Access Control
        self.enforce_access_control_checkbox = QCheckBox("Enforce Access Control")
        access_layout.addWidget(self.enforce_access_control_checkbox)

        # Working Hours
        working_hours_layout = QHBoxLayout()
        working_hours_label = QLabel("Working Hours:")
        self.working_hours_input = QLineEdit("08:00-17:00")  # Default value
        working_hours_layout.addWidget(working_hours_label)
        working_hours_layout.addWidget(self.working_hours_input)
        access_layout.addLayout(working_hours_layout)

        # Workday Start Time
        start_time_layout = QHBoxLayout()
        start_time_label = QLabel("Workday Start Time:")
        self.workday_start_time_input = QTimeEdit()
        self.workday_start_time_input.setTime(QTime(8, 0))  # Default time
        start_time_layout.addWidget(start_time_label)
        start_time_layout.addWidget(self.workday_start_time_input)
        access_layout.addLayout(start_time_layout)

        # Workday End Time
        end_time_layout = QHBoxLayout()
        end_time_label = QLabel("Workday End Time:")
        self.workday_end_time_input = QTimeEdit()
        self.workday_end_time_input.setTime(QTime(17, 0))  # Default time
        end_time_layout.addWidget(end_time_label)
        end_time_layout.addWidget(self.workday_end_time_input)
        access_layout.addLayout(end_time_layout)

        access_tab.setLayout(access_layout)
        return access_tab

    def create_database_tab(self):
        """Create the Database settings tab"""
        database_tab = QWidget()
        database_layout = QVBoxLayout()

        # Database Type
        db_type_layout = QHBoxLayout()
        db_type_label = QLabel("Database Type:")
        self.db_type_combo = QComboBox()
        self.db_type_combo.addItems(["CSV", "MySQL"])  # Example options
        self.db_type_combo.currentIndexChanged.connect(self.update_database_fields)  # Connect to handler
        db_type_layout.addWidget(db_type_label)
        db_type_layout.addWidget(self.db_type_combo)
        database_layout.addLayout(db_type_layout)

        # Container for database input fields
        self.database_input_layout = QVBoxLayout()
        database_layout.addLayout(self.database_input_layout)

        # Initial field setup
        self.update_database_fields()  # Set up fields based on default selection

        database_tab.setLayout(database_layout)
        return database_tab

    def update_database_fields(self):
        """Update database input fields based on the selected database type"""
        # Clear previous fields
        for i in reversed(range(self.database_input_layout.count())):
            widget = self.database_input_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        db_type = self.db_type_combo.currentText()

        if db_type == "CSV":
            # CSV settings
            csv_file_layout = QHBoxLayout()
            csv_file_label = QLabel("CSV File Path:")
            self.csv_file_input = QLineEdit("path/to/your/file.csv")  # Default value
            csv_file_layout.addWidget(csv_file_label)
            csv_file_layout.addWidget(self.csv_file_input)
            self.database_input_layout.addLayout(csv_file_layout)

            delimiter_layout = QHBoxLayout()
            delimiter_label = QLabel("Delimiter:")
            self.delimiter_input = QLineEdit(",")  # Default delimiter
            delimiter_layout.addWidget(delimiter_label)
            delimiter_layout.addWidget(self.delimiter_input)
            self.database_input_layout.addLayout(delimiter_layout)

        elif db_type in ["SQLite", "MySQL", "PostgreSQL"]:
            # SQL Database settings
            connection_string_layout = QHBoxLayout()
            connection_string_label = QLabel("Connection String:")
            self.connection_string_input = QLineEdit("localhost:3306/mydatabase")  # Default value
            connection_string_layout.addWidget(connection_string_label)
            connection_string_layout.addWidget(self.connection_string_input)
            self.database_input_layout.addLayout(connection_string_layout)

            # Connection Pooling
            self.enable_pooling_checkbox = QCheckBox("Enable Connection Pooling")
            self.database_input_layout.addWidget(self.enable_pooling_checkbox)

        # Test Connection Button
        self.test_connection_button = QPushButton("Test Connection")
        self.test_connection_button.clicked.connect(self.test_database_connection)
        self.database_input_layout.addWidget(self.test_connection_button)

    def create_database_tab(self):
        """Create the Database settings tab"""
        database_tab = QWidget()
        database_layout = QVBoxLayout()

        # Database Type
        db_type_layout = QHBoxLayout()
        db_type_label = QLabel("Database Type:")
        self.db_type_combo = QComboBox()
        self.db_type_combo.addItems(["CSV",  "MySQL"])  # Example options
        self.db_type_combo.currentIndexChanged.connect(self.update_database_fields)  # Connect to handler
        db_type_layout.addWidget(db_type_label)
        db_type_layout.addWidget(self.db_type_combo)
        database_layout.addLayout(db_type_layout)

        # Container for database input fields
        self.database_input_layout = QVBoxLayout()
        database_layout.addLayout(self.database_input_layout)

        # Initial field setup
        self.update_database_fields()  # Set up fields based on default selection

        database_tab.setLayout(database_layout)
        return database_tab

    def update_database_fields(self):
        """Update database input fields based on the selected database type"""
        # Clear previous fields
        for i in reversed(range(self.database_input_layout.count())):
            widget = self.database_input_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        db_type = self.db_type_combo.currentText()

        if db_type == "CSV":
            # CSV settings
            csv_file_layout = QHBoxLayout()
            csv_file_label = QLabel("CSV File Path:")
            self.csv_file_input = QLineEdit("path/to/your/file.csv")  # Default value
            csv_file_layout.addWidget(csv_file_label)
            csv_file_layout.addWidget(self.csv_file_input)
            self.database_input_layout.addLayout(csv_file_layout)

            delimiter_layout = QHBoxLayout()
            delimiter_label = QLabel("Delimiter:")
            self.delimiter_input = QLineEdit(",")  # Default delimiter
            delimiter_layout.addWidget(delimiter_label)
            delimiter_layout.addWidget(self.delimiter_input)
            self.database_input_layout.addLayout(delimiter_layout)

        elif db_type in ["SQLite", "MySQL", "PostgreSQL"]:
            # SQL Database settings
            connection_string_layout = QHBoxLayout()
            connection_string_label = QLabel("Connection String:")
            self.connection_string_input = QLineEdit("localhost:3306/mydatabase")  # Default value
            connection_string_layout.addWidget(connection_string_label)
            connection_string_layout.addWidget(self.connection_string_input)
            self.database_input_layout.addLayout(connection_string_layout)

            # Connection Pooling
            self.enable_pooling_checkbox = QCheckBox("Enable Connection Pooling")
            self.database_input_layout.addWidget(self.enable_pooling_checkbox)

        # Test Connection Button
        self.test_connection_button = QPushButton("Test Connection")
        self.test_connection_button.clicked.connect(self.test_database_connection)
        self.database_input_layout.addWidget(self.test_connection_button)

    def test_database_connection(self):
        """Test the database connection (placeholder implementation)"""
        db_type = self.db_type_combo.currentText()

        if db_type == "CSV":
            file_path = self.csv_file_input.text()
            delimiter = self.delimiter_input.text()
            print(f"Testing connection to CSV file at: {file_path} with delimiter: {delimiter}")
            # Add actual CSV handling logic here

        else:
            connection_string = self.connection_string_input.text()
            enable_pooling = self.enable_pooling_checkbox.isChecked()
            print(f"Testing connection to {db_type} with string: {connection_string}")
            print(f"Connection pooling enabled: {enable_pooling}")
            # Add actual database connection testing logic here

    def save_settings(self):
        """Logic to save settings can be added here"""
        camera_index = self.camera_index_input.text()
        resolution = self.resolution_combo.currentText()
        brightness_control_enabled = self.brightness_control_checkbox.isChecked()
        date_format = self.date_format_combo.currentText()
        time_format = self.time_format_combo.currentText()
        enforce_access_control = self.enforce_access_control_checkbox.isChecked()
        working_hours = self.working_hours_input.text()
        workday_start_time = self.workday_start_time_input.time().toString()
        workday_end_time = self.workday_end_time_input.time().toString()

        print(f"settings saved: Camera Index - {camera_index}, Resolution - {resolution}, Brightness Control - {brightness_control_enabled}")
        print(f"Date Format - {date_format}, Time Format - {time_format}")
        print(f"Access Control - {enforce_access_control}, Working Hours - {working_hours}, Start Time - {workday_start_time}, End Time - {workday_end_time}")
        self.accept()
