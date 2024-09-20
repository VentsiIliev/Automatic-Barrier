from pathlib import Path
import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QTimeEdit
from PyQt5.QtCore import QTime
from control_panel import Constants
from control_panel.BaseLayout import BaseLayout
from control_panel.enums.AccessEventType import AccessEventType


class ReportsLayout(BaseLayout):
    def __init__(self, parent=None):
        super().__init__("Reports", parent)
        self.initUI()

    def initUI(self):
        """Initialize the reports layout."""
        # Add input fields (filters)
        self.registrationInput = self.addInputField("Registration Number")
        self.dateInput = self.addDateField("Date")  # Changed to Date Edit field
        self.timeFromInput = self.addTimeField("From Time")  # "From" time field
        self.timeToInput = self.addTimeField("To Time")      # "To" time field
        self.directionInput = self.addComboBox(["All", "IN", "OUT"])
        self.accessLevelInput = self.addComboBox(["All", "Admin", "User", "Guest"])
        self.accessStatusInput = self.addComboBox(["All", "GRANTED", "DENIED"])

        # Add Generate Report Button
        self.addButton("Generate Report", self.generateReport)

        # Add Report Table
        self.addTable(6, ["Registration", "Date", "Time", "Direction", "Access Level", "Access Status"])

    def addTimeField(self, placeholder):
        """Add a time field with a calendar popup."""
        time_field = QTimeEdit(self)
        time_field.setDisplayFormat("hh:mm:ss")
        time_field.setTime(QTime.currentTime())  # Set default to current time
        self.layout.addWidget(time_field)
        return time_field

    def generateReport(self):
        try:
            reg = self.registrationInput.text().upper()
            date_input = self.dateInput.date().toString("yyyy-MM-dd")
            time_from_input = self.timeFromInput.time().toString("hh:mm:ss")
            time_to_input = self.timeToInput.time().toString("hh:mm:ss")
            direction = self.directionInput.currentText()
            access_status = self.accessStatusInput.currentText()

            # Prepare file paths
            base_directory = Path(__file__).resolve().parent.parent  # Go up two levels
            database_directory = base_directory / 'database'

            access_granted_path = database_directory / Constants.ACCESS_GRANTED_TABLE
            access_denied_path = database_directory / Constants.ACCESS_DENIED_TABLE

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

            # Filter based on access status (GRANTED or DENIED)
            if access_status == "GRANTED":
                data = data_granted
            elif access_status == "DENIED":
                data = data_denied
            else:
                data = pd.concat([data_granted, data_denied])

            # Apply additional filters
            if reg:
                data = data[data['Registration Number'].str.upper() == reg]

            if direction and direction != "All":
                data = data[data['Direction'] == direction]

            if date_input:
                data = data[data['Date'] == date_input]

            # Filter by time range
            if time_from_input and time_to_input:
                data = data[(data['Time'] >= time_from_input) & (data['Time'] <= time_to_input)]

            # Populate the report table
            self.populateReportTable(data)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def populateReportTable(self, data):
        """Populate the report table with the filtered data."""
        self.table.setRowCount(len(data))
        for row in range(len(data)):
            self.table.setItem(row, 0, QTableWidgetItem(data.iloc[row]['Registration Number']))
            self.table.setItem(row, 1, QTableWidgetItem(data.iloc[row]['Date']))
            self.table.setItem(row, 2, QTableWidgetItem(data.iloc[row]['Time']))
            self.table.setItem(row, 3, QTableWidgetItem(data.iloc[row]['Direction']))
            self.table.setItem(row, 4, QTableWidgetItem(data.iloc[row]['Event Type']))  # Assuming 'Event Type' contains Access Level
            # self.table.setItem(row, 5, QTableWidgetItem(data.iloc[row]['Access Status']))  # Assuming this field is available
