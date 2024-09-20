import os
from pathlib import Path
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, \
    QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit, QTimeEdit
import pandas as pd

from control_panel import Constants
from control_panel.BaseLayout import BaseLayout
from control_panel.enums.AccessEventType import AccessEventType


class ReportsLayout(BaseLayout):
    def __init__(self, parent=None):
        super().__init__("Reports",parent)
        self.initUI()

    def initUI(self):
        """Initialize the reports layout."""

        # Add input fields (filters)
        self.registrationInput = self.addInputField("Registration Number")
        self.dateInput = self.addInputField("Date")
        self.timeInput = self.addInputField("Time")
        self.directionInput = self.addComboBox(["", "IN", "OUT"])
        self.accessLevelInput = self.addComboBox(["", "Admin", "User", "Guest"])
        self.accessStatusInput = self.addComboBox(["", "GRANTED", "DENIED"])

        # Add Generate Report Button
        self.addButton("Generate Report", self.generateReport)

        # Add Report Table
        self.addTable(6, ["Registration", "Date", "Time", "Direction", "Access Level", "Access Status"])

    def generateReport(self):
        try:
            reg = self.registrationInput.text().upper()

            # Retrieve date and time from QDateEdit and QTimeEdit
            date_time = self.dateInput.date().toString("yyyy-MM-dd") + " " + self.timeInput.time().toString("hh:mm:ss")

            direction = self.directionInput.currentText()
            access_status = self.accessStatusInput.currentText()

            # Prepare file paths
            base_directory = Path(__file__).resolve().parent.parent  # This goes up two levels
            database_directory = base_directory / 'database'  # Ensure this points to the right location
            access_granted_path = database_directory / Constants.ACCESS_GRANTED_TABLE
            access_denied_path = database_directory / Constants.ACCESS_DENIED_TABLE
            whitelisted_vehicles_path = database_directory / Constants.WHITELISTED_VEHICLES_TABLE

            # Check if files exist
            if not access_granted_path.exists():
                QMessageBox.warning(self, "File Not Found", f"File not found: {access_granted_path}")
                return
            if not access_denied_path.exists():
                QMessageBox.warning(self, "File Not Found", f"File not found: {access_denied_path}")
                return

            # Load data
            data_granted = pd.read_csv(access_granted_path)
            data_denied = pd.read_csv(access_denied_path)
            whitelisted_vehicles = pd.read_csv(whitelisted_vehicles_path, delimiter=';')

            # Filter data based on access status
            if access_status == AccessEventType.GRANTED.value:
                data = data_granted
            elif access_status == AccessEventType.DENIED.value:
                data = data_denied
            else:
                data = pd.concat([data_granted, data_denied])

            # Apply additional filters
            if reg:
                data = data[data['Registration Number'].str.upper() == reg]

            if direction and direction != "All":
                data = data[data['Direction'] == direction]

            # Populate the report table
            self.populateReportTable(data)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    # def populateReportTable(self, data):
    #     """Populate the report table with the filtered data."""
    #     self.reportTable.setRowCount(len(data))
    #
    #     for row in range(len(data)):
    #         self.reportTable.setItem(row, 0, QTableWidgetItem(data.iloc[row]['Registration Number']))
    #         self.reportTable.setItem(row, 1, QTableWidgetItem(data.iloc[row]['Date']))
    #         self.reportTable.setItem(row, 2, QTableWidgetItem(data.iloc[row]['Time']))
    #         self.reportTable.setItem(row, 3, QTableWidgetItem(data.iloc[row]['Direction']))
    #         self.reportTable.setItem(row, 4, QTableWidgetItem(data.iloc[row]['Event Type']))  # Assuming 'Event Type' contains Access Level
    #         # self.reportTable.setItem(row, 5, QTableWidgetItem(data.iloc[row]['Access Status']))  # Adjusted based on file structure
