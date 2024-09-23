from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QLabel, QSizePolicy
from PyQt5.QtGui import QFont

from core_system.view.settings_window.conreate_tabs.AccessControlTab import AccessControlTab
from core_system.view.settings_window.conreate_tabs.CameraSettingsTab import CameraTab
from core_system.view.settings_window.conreate_tabs.DatabaseTab import DatabaseTab
from core_system.view.settings_window.conreate_tabs.DatetimeSettingsTab import DateTimeTab
from core_system.view.settings_window.conreate_tabs.SystemSettingsTab import SystemTab


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 600, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #f4f4f9;
                color: #333;
            }
            QLabel {
                font-size: 14px;
                color: #555;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 8px;
                border: none;
                height: 40px;  /* Fixed height for buttons */
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: #fff;
                border-radius: 10px;
                margin-top: 10px;
            }
            QTabBar::tab {
                padding: 10px 15px;
                font-size: 14px;
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-right: 5px;
                min-width: 100px;  /* Minimum width for tabs */
            }
            QTabBar::tab:selected {
                background-color: #fff;
                border-bottom: 2px solid #007BFF;
            }
        """)

        layout = QVBoxLayout()

        # Header
        header = QLabel("Settings")
        header.setFont(QFont("Arial", 22, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #007BFF; padding: 10px 0;")
        layout.addWidget(header)

        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(CameraTab(), "Camera")
        self.tab_widget.addTab(SystemTab(), "System")
        self.tab_widget.addTab(DateTimeTab(), "Date & Time")
        self.tab_widget.addTab(AccessControlTab(), "Access Control")
        self.tab_widget.addTab(DatabaseTab(), "Database")

        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

        # Adjust the tab widget size policy to ensure proper resizing
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)