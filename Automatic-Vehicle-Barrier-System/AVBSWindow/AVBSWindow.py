import sys
import cv2
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QGridLayout
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt

class AVBSWindow(QWidget):
    def __init__(self, barrier_control):
        super().__init__()
        self.barrier_control = barrier_control

        # Setup the window
        self.setWindowTitle("AVBS - Automated Vehicle Barrier System")
        self.setStyleSheet("background-color: #2c3e50; color: #ecf0f1;")
        self.setGeometry(100, 100, 1280, 720)

        # Main layout
        main_layout = QVBoxLayout()

        # Header
        header = QLabel("Automated Vehicle Barrier System")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #ecf0f1; padding: 10px; background-color: #34495e; border-radius: 5px;")
        main_layout.addWidget(header)

        # Horizontal layout for camera feed and info panel
        camera_info_layout = QHBoxLayout()

        # Camera feed label (styled with a border and padding)
        self.camera_label = QLabel(self)
        self.camera_label.setFrameShape(QFrame.Box)
        self.camera_label.setStyleSheet("border: 2px solid #2980b9; padding: 5px;")
        self.camera_label.setFixedSize(640, 360)  # Set a fixed size for better layout control
        camera_info_layout.addWidget(self.camera_label)

        # Info Panel
        self.info_panel = self.create_info_panel()
        camera_info_layout.addLayout(self.info_panel)

        # Add camera and info layout to main layout
        main_layout.addLayout(camera_info_layout)

        # Add manual barrier control buttons
        self.add_manual_controls(main_layout)

        self.setLayout(main_layout)

    def create_info_panel(self):
        """ Create a panel to display event information in a more polished way """
        info_layout = QVBoxLayout()

        # Detected vehicle image (QLabel)
        self.vehicle_image_label = QLabel(self)
        self.vehicle_image_label.setFixedSize(300, 300)
        self.vehicle_image_label.setStyleSheet("border: 2px solid #27ae60;")
        info_layout.addWidget(self.vehicle_image_label, alignment=Qt.AlignCenter)

        # Event type label
        self.event_type_label = QLabel("Event Type: N/A")
        self.event_type_label.setFont(QFont("Arial", 14))
        info_layout.addWidget(self.event_type_label)

        # Timestamp label
        self.timestamp_label = QLabel("Timestamp: N/A")
        self.timestamp_label.setFont(QFont("Arial", 14))
        info_layout.addWidget(self.timestamp_label)

        # License plate label
        self.license_plate_label = QLabel("License Plate: N/A")
        self.license_plate_label.setFont(QFont("Arial", 14))
        info_layout.addWidget(self.license_plate_label)

        # Direction label (IN/OUT)
        self.direction_label = QLabel("Direction: N/A")
        self.direction_label.setFont(QFont("Arial", 14))
        info_layout.addWidget(self.direction_label)

        # Vehicles on premises count
        self.vehicles_on_premises_label = QLabel("Vehicles on Premises: 0")
        self.vehicles_on_premises_label.setFont(QFont("Arial", 14))
        info_layout.addWidget(self.vehicles_on_premises_label)

        return info_layout

    def add_manual_controls(self, layout):
        """ Add buttons for manual barrier control """
        button_layout = QHBoxLayout()

        # Open Barrier button
        self.open_barrier_button = QPushButton("Open Barrier")
        self.open_barrier_button.setStyleSheet("background-color: #27ae60; color: white; font-size: 16px;")
        self.open_barrier_button.setFixedHeight(50)
        self.open_barrier_button.clicked.connect(self.barrier_control.open)
        button_layout.addWidget(self.open_barrier_button)

        # Close Barrier button
        self.close_barrier_button = QPushButton("Close Barrier")
        self.close_barrier_button.setStyleSheet("background-color: #e74c3c; color: white; font-size: 16px;")
        self.close_barrier_button.setFixedHeight(50)
        self.close_barrier_button.clicked.connect(self.barrier_control.close)
        button_layout.addWidget(self.close_barrier_button)

        # Add buttons to the layout
        layout.addLayout(button_layout)

    def update_camera_feed(self, frame):
        """Updates the camera feed QLabel with the given frame"""
        if frame is not None:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            self.camera_label.setPixmap(QPixmap.fromImage(q_image).scaled(self.camera_label.size(), Qt.KeepAspectRatio))

    def update_info_panel(self, event, vehicle_image, vehicles_on_premises_count):
        """ Updates the info panel with event details and the vehicle image """
        if event:
            # Update event information
            self.event_type_label.setText(f"Event Type: {event.type.name}")
            self.timestamp_label.setText(f"Timestamp: {event.time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.license_plate_label.setText(f"License Plate: {event.registration_number}")
            self.direction_label.setText(f"Direction: {event.direction}")
            self.vehicles_on_premises_label.setText(f"Vehicles on Premises: {vehicles_on_premises_count}")

            # Update vehicle image
            vehicle_height, vehicle_width, _ = vehicle_image.shape
            vehicle_bytes = vehicle_image.tobytes()  # Convert numpy array to bytes
            vehicle_qimage = QImage(vehicle_bytes, vehicle_width, vehicle_height, vehicle_width * 3,
                                    QImage.Format_RGB888).rgbSwapped()
            self.vehicle_image_label.setPixmap(
                QPixmap.fromImage(vehicle_qimage).scaled(self.vehicle_image_label.size(), Qt.KeepAspectRatio))

    def closeEvent(self, event):
        self.barrier_control.stop()
        event.accept()
