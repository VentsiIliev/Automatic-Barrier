import traceback
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QTimeEdit
from PyQt5.QtCore import QTime

from control_panel.BaseLayout import BaseLayout
from control_panel.data_managment.Filter import Filter
from control_panel.data_managment.ReportGenerator import ReportsGenerator
from repositories.csv_repositories.Constants import DATE, TIME, REGISTRATION_NUMBER, DIRECTION


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
        self.timeToInput = self.addTimeField("To Time")  # "To" time field
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

    def create_filters(self):
        """Gather filter input from the UI and return a dictionary."""
        filters = Filter(
            registration_number=self.registrationInput.text().upper() or None,
            date_range=(self.dateInput.date().toString("yyyy-MM-dd"),) if self.dateInput.date() else None,
            time_range=(self.timeFromInput.time().toString("hh:mm:ss"), self.timeToInput.time().toString("hh:mm:ss"))
            if self.timeFromInput.time() and self.timeToInput.time() else None,
            direction=self.directionInput.currentText() if self.directionInput.currentText() != "All" else None,
            access_status=self.accessStatusInput.currentText() if self.accessStatusInput.currentText() != "All" else None
        )
        return filters

    def generateReport(self):
        try:
            report_generator = ReportsGenerator()
            # Gather filter input from the UI
            filters = self.create_filters()
            # Generate the report using ReportsGenerator
            data = report_generator.generate_report(filters.to_dict())
            # Populate the report table
            self.populateReportTable(data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            traceback.print_exc()

    def populateReportTable(self, data):
        """Populate the report table with the filtered data."""
        self.table.setRowCount(len(data))
        for row in range(len(data)):
            self.table.setItem(row, 0, QTableWidgetItem(data.iloc[row][REGISTRATION_NUMBER]))
            self.table.setItem(row, 1, QTableWidgetItem(data.iloc[row][DATE]))
            self.table.setItem(row, 2, QTableWidgetItem(data.iloc[row][TIME]))
            self.table.setItem(row, 3, QTableWidgetItem(data.iloc[row][DIRECTION]))
            # self.table.setItem(row, 4, QTableWidgetItem(data.iloc[row][ACCESS_LEVEL]))  # Assuming 'Access Level' is under 'Event Type'
