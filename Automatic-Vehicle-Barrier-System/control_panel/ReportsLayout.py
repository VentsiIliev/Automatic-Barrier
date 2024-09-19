import os
from pathlib import Path
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, \
    QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit, QTimeEdit
import pandas as pd

from control_panel import Constants
from control_panel.enums.AccessEventType import AccessEventType


class ReportsLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        """Initialize the reports layout."""
        layout = QVBoxLayout()

        # Reports Title
        titleLabel = QLabel("Reports", self)
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(titleLabel)

        # Filters Section
        filterLayout = QVBoxLayout()

        # Registration Number Filter
        self.registrationInput = QLineEdit(self)
        self.registrationInput.setPlaceholderText("Registration Number")
        filterLayout.addWidget(self.registrationInput)

        # Date Filter
        self.dateInput = QDateEdit(self)
        self.dateInput.setDate(QDate.currentDate())
        filterLayout.addWidget(self.dateInput)

        # Time Filter
        self.timeInput = QTimeEdit(self)
        self.timeInput.setTime(QTime.currentTime())
        filterLayout.addWidget(self.timeInput)

        # Direction Filter
        self.directionInput = QComboBox(self)
        self.directionInput.addItems(["", "IN", "OUT"])
        filterLayout.addWidget(self.directionInput)

        # Access Level Filter
        self.accessLevelInput = QComboBox(self)
        self.accessLevelInput.addItems(["", "Admin", "User", "Guest"])
        filterLayout.addWidget(self.accessLevelInput)

        # Access Status Filter
        self.accessStatusInput = QComboBox(self)
        self.accessStatusInput.addItems(["", "GRANTED", "DENIED"])
        filterLayout.addWidget(self.accessStatusInput)

        # Generate Report Button
        generateReportButton = QPushButton("Generate Report", self)
        generateReportButton.clicked.connect(self.generateReport)
        filterLayout.addWidget(generateReportButton)

        layout.addLayout(filterLayout)

        # Reports Table
        self.reportTable = QTableWidget()
        self.reportTable.setColumnCount(6)
        self.reportTable.setHorizontalHeaderLabels(
            ["Registration", "Date", "Time", "Direction", "Access Level", "Access Status"]
        )
        layout.addWidget(self.reportTable)

        self.setLayout(layout)

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
            print(f"Access Granted Path: {access_granted_path.resolve()}")

            access_denied_path = database_directory / Constants.ACCESS_DENIED_TABLE
            whitelisted_vehicles_path = database_directory / Constants.WHITELISTED_VEHICLES_TABLE

            # Check if files exist
            if not access_granted_path.exists():
                QMessageBox.warning(self, "File Not Found", f"File not found: {access_granted_path}")
                return
            if not access_denied_path.exists():
                QMessageBox.warning(self, "File Not Found", f"File not found: {access_denied_path}")
                return
            # if not whitelisted_vehicles_path.exists():
            #     QMessageBox.warning(self, "File Not Found", f"File not found: {whitelisted_vehicles_path}")
            #     return

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
            # if date_time:
            #     data = data[data['Date Time'].str.startswith(date_time)]
            if direction and direction != "All":
                data = data[data['Direction'] == direction]

            # Populate the report table
            self.populateReportTable(data)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def populateReportTable(self, data):
        """Populate the report table with the filtered data."""
        # Print the columns to verify their names
        print("DataFrame columns:", data.columns.tolist())

        self.reportTable.setRowCount(len(data))

        for row in range(len(data)):
            self.reportTable.setItem(row, 0, QTableWidgetItem(data.iloc[row]['Registration Number']))  # Adjusted
            self.reportTable.setItem(row, 1, QTableWidgetItem(data.iloc[row]['Date Time']))  # Adjusted
            self.reportTable.setItem(row, 2, QTableWidgetItem(data.iloc[row]['Direction']))  # Adjusted
            # self.reportTable.setItem(row, 3, QTableWidgetItem(data.iloc[row]['Access Level']))  # Adjusted
            # self.reportTable.setItem(row, 4, QTableWidgetItem(data.iloc[row]['Access Status']))  # Adjusted
