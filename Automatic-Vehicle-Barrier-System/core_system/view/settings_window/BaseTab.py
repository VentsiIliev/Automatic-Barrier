from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel


class BaseTab(QWidget):
    def __init__(self, ):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)  # Set padding for all tabs
        self.setLayout(self.layout)

        # self.add_save_button()

    def add_save_button(self):
        # Define the Save settings button before adding it to the layout
        self.save_button = QPushButton("Save settings")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

    def add_form_row(self, label_text, widget):
        row_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; color: #007BFF;")
        row_layout.addWidget(label)
        row_layout.addWidget(widget)
        self.layout.addLayout(row_layout)

    def save_settings(self):
        """Default save settings method, can be overridden."""
        print("Save settings logic needs to be implemented in the concrete tab.")
