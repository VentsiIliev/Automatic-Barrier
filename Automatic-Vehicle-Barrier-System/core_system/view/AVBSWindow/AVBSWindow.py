import sys
import time
import traceback

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QGridLayout, \
    QToolBar, QAction, QMainWindow, QSizePolicy, QCheckBox, QSpacerItem
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt

from core_system.view.settings_window.SettingsWindow import SettingsWindow


class AVBSWindow(QMainWindow):
    WINDOW_TITLE = "AVBS - Automated Vehicle Barrier System"
    SYSTEM_STATUS_ONLINE = "System Online"
    SYSTEM_STATUS_OFFLINE = "System Offline"
    def __init__(self, barrier_control):
        super().__init__()
        self.barrier_control = barrier_control
        self.last_frame_time = time.time()

        # Setup the window
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setStyleSheet("background-color: #f9f9f9; color: #4c4c4c;")
        self.setGeometry(100, 100, 1280, 720)

        # State to track manual control
        self.manual_control_enabled = True  # Default to manual control enabled

        # Main widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Add a status bar
        self.statusBar().showMessage(self.SYSTEM_STATUS_ONLINE)

        # Quick Access Toolbar
        self.create_quick_access_toolbar()

        # Camera feed and Info Panel
        camera_info_layout = QHBoxLayout()

        # Camera feed label (styled with a border and padding)
        self.camera_label = QLabel(self)
        self.camera_label.setFrameShape(QFrame.Box)
        self.camera_label.setStyleSheet("border: 2px solid #4c87b9; padding: 5px; border-radius: 10px;")
        self.camera_label.setFixedSize(640, 360)  # Fixed size for the camera feed
        camera_info_layout.addWidget(self.camera_label)

        # Info panel layout
        info_panel = self.create_info_panel()
        camera_info_layout.addWidget(info_panel)

        main_layout.addLayout(camera_info_layout)

        # Add manual control toggle
        self.add_manual_control_toggle(main_layout)

        # Add manual barrier control buttons (toggled on/off based on checkbox)
        self.add_manual_controls(main_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_quick_access_toolbar(self):
        """Creates a quick access toolbar"""
        toolbar = QToolBar("Quick Access Toolbar")
        self.addToolBar(toolbar)

        # Open Barrier button
        open_action = QAction("Open Barrier", self)
        open_action.triggered.connect(self.barrier_control.open)
        toolbar.addAction(open_action)

        # Close Barrier button
        close_action = QAction("Close Barrier", self)
        close_action.triggered.connect(self.barrier_control.close)
        toolbar.addAction(close_action)

        # Settings Action (placeholder)
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)  # Make sure this method exists
        toolbar.addAction(settings_action)

        # View Logs Action
        logs_action = QAction("View Logs", self)
        logs_action.triggered.connect(self.view_logs)  # Ensure this method exists
        toolbar.addAction(logs_action)

        # Exit Action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_application)
        toolbar.addAction(exit_action)

    def open_settings(self):
        print("Open settings clicked")
        # settings_window = SettingsWindow(self.settings_manager)
        try:
            settings_window = SettingsWindow()
            settings_window.exec_()
        except Exception as e:
            traceback.print_exc()
            print("Failed to open settings window:", e)



    def view_logs(self):
        print("View logs clicked")
        # Code to view logs can be added here

    def exit_application(self):
        print("Exit clicked")
        QApplication.instance().quit()

    def create_info_panel(self):
        """ Create an info panel with a grid layout for better structure """
        info_panel = QFrame()
        info_panel.setStyleSheet("""
            border: 2px solid #dcdcdc;
            padding: 10px;
            background-color: #ffffff;
            border-radius: 8px;
        """)
        info_layout = QGridLayout()

        # Detected vehicle image
        self.vehicle_image_label = QLabel(self)
        self.vehicle_image_label.setFixedSize(200, 150)
        self.vehicle_image_label.setStyleSheet("""
            border: 2px solid #27ae60;
            border-radius: 5px;
        """)
        info_layout.addWidget(self.vehicle_image_label, 0, 0, 2, 1)

        # Event info labels
        labels = {
            'Event Type': 'N/A',
            'Timestamp': 'N/A',
            'License Plate': 'N/A',
            'Direction': 'N/A',
            'Vehicles on Premises': '0',
            'Camera FPS': '0 FPS'  # Added FPS label
        }
        self.info_labels = {}

        row = 0
        for key, value in labels.items():
            label_title = QLabel(f"{key}:")
            label_title.setFont(QFont("Arial", 14))
            label_title.setStyleSheet("color: #4c4c4c; font-weight: bold;")
            info_layout.addWidget(label_title, row, 1)

            label_value = QLabel(value)
            label_value.setFont(QFont("Arial", 14))
            label_value.setStyleSheet("color: #4c4c4c;")
            self.info_labels[key] = label_value
            info_layout.addWidget(label_value, row, 2)

            row += 1

        info_panel.setLayout(info_layout)
        return info_panel

    def add_manual_control_toggle(self, layout):
        """ Add a toggle for manual control """
        manual_control_layout = QHBoxLayout()
        self.manual_control_checkbox = QCheckBox("Enable Manual Control")
        self.manual_control_checkbox.setChecked(self.manual_control_enabled)
        self.manual_control_checkbox.stateChanged.connect(self.toggle_manual_control)
        self.manual_control_checkbox.setStyleSheet("font-size: 14px; margin: 10px;")

        manual_control_layout.addWidget(self.manual_control_checkbox)
        # Add a spacer to align it in the center
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        manual_control_layout.addSpacerItem(spacer)
        layout.addLayout(manual_control_layout)

    def toggle_manual_control(self, state):
        """ Toggle the manual control on/off """
        self.manual_control_enabled = state == Qt.Checked
        self.open_barrier_button.setVisible(self.manual_control_enabled)
        self.close_barrier_button.setVisible(self.manual_control_enabled)

    def add_manual_controls(self, layout):
        """ Add buttons for manual barrier control """
        self.manual_control_buttons_layout = QHBoxLayout()

        # Open Barrier button
        self.open_barrier_button = QPushButton("Open Barrier")
        self.open_barrier_button.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 10px;
        """)
        self.open_barrier_button.setFixedHeight(50)
        self.open_barrier_button.clicked.connect(self.barrier_control.open)
        self.manual_control_buttons_layout.addWidget(self.open_barrier_button)

        # Close Barrier button
        self.close_barrier_button = QPushButton("Close Barrier")
        self.close_barrier_button.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 10px;
        """)
        self.close_barrier_button.setFixedHeight(50)
        self.close_barrier_button.clicked.connect(self.barrier_control.close)
        self.manual_control_buttons_layout.addWidget(self.close_barrier_button)

        # Add the buttons layout to the main layout
        layout.addLayout(self.manual_control_buttons_layout)

        # Initially set buttons visible or hidden based on manual control state
        self.open_barrier_button.setVisible(self.manual_control_enabled)
        self.close_barrier_button.setVisible(self.manual_control_enabled)

    def exit_application(self):
        print("Exit clicked")
        sys.exit(1)

    def update_camera_feed(self, frame):
        """Updates the camera feed QLabel with the given frame and updates the FPS display."""
        if frame is not None:
            # Calculate FPS
            current_time = time.time()
            fps = 1.0 / (current_time - self.last_frame_time)
            self.last_frame_time = current_time

            # Update FPS in the info panel
            self.info_labels['Camera FPS'].setText(f"{fps:.2f} FPS")

            # Update the camera feed display
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            self.camera_label.setPixmap(QPixmap.fromImage(q_image).scaled(self.camera_label.size(), Qt.KeepAspectRatio))

    def update_info_panel(self, event, vehicle_image, vehicles_on_premises_count):
        """ Updates the info panel with event details and the vehicle image """
        if event:
            self.info_labels['Event Type'].setText(event.type.name)
            self.info_labels['Timestamp'].setText(event.time.strftime('%Y-%m-%d %H:%M:%S'))
            self.info_labels['License Plate'].setText(event.registration_number)
            self.info_labels['Direction'].setText(event.direction)
            self.info_labels['Vehicles on Premises'].setText(str(vehicles_on_premises_count))

            vehicle_height, vehicle_width, _ = vehicle_image.shape
            vehicle_bytes = vehicle_image.tobytes()
            vehicle_qimage = QImage(vehicle_bytes, vehicle_width, vehicle_height, vehicle_width * 3,
                                    QImage.Format_RGB888).rgbSwapped()
            self.vehicle_image_label.setPixmap(
                QPixmap.fromImage(vehicle_qimage).scaled(self.vehicle_image_label.size(), Qt.KeepAspectRatio))

    def closeEvent(self, event):
        self.barrier_control.stop()
        event.accept()
