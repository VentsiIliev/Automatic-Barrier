import traceback

from PyQt5.QtCore import QTime, QDate
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QPushButton, QLineEdit, QComboBox, QDateEdit, \
    QTimeEdit, QTableWidgetItem, QMessageBox

from admin_dashboard.data_managment.ReportGenerator import ReportsGenerator


class BaseLayout(QWidget):
    def __init__(self, title, table_headers, parent=None):
        super().__init__(parent)
        self.title = title
        self.table_headers = table_headers
        self.initBaseUI()

    def initBaseUI(self):
        """Initialize the base layout."""
        self.layout = QVBoxLayout()

        # Title
        titleLabel = QLabel(self.title, self)
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(titleLabel)

        self.setLayout(self.layout)

    def addTable(self, column_count, headers):
        """Add a table widget to the layout."""
        self.table = QTableWidget(self)
        self.table.setColumnCount(column_count)
        self.table.setHorizontalHeaderLabels(headers)
        self.layout.addWidget(self.table)

    def addInputField(self, placeholder):
        """Add an input field to the layout."""
        input_field = QLineEdit(self)
        input_field.setPlaceholderText(placeholder)
        self.layout.addWidget(input_field)
        return input_field

    def addComboBox(self, items):
        """Add a combo box with specified items."""
        combo = QComboBox(self)
        combo.addItems(items)
        self.layout.addWidget(combo)
        return combo

    def addButton(self, label, callback):
        """Add a button to the layout."""
        button = QPushButton(label, self)
        button.clicked.connect(callback)
        self.layout.addWidget(button)
        return button

    def addDateField(self, placeholder):
        """Add a date field with a calendar popup and default to the current date."""
        date_field = QDateEdit(self)
        date_field.setDisplayFormat("yyyy-MM-dd")
        date_field.setCalendarPopup(True)  # Enables the calendar popup
        date_field.setDate(QDate.currentDate())  # Sets the current date as default
        self.layout.addWidget(date_field)
        return date_field

    def addTimeField(self, placeholder):
        """Add a time field to the layout."""
        time_field = QTimeEdit(self)
        time_field.setDisplayFormat("hh:mm:ss")  # Set the time display format
        time_field.setTime(QTime.currentTime())  # Optional: set the current time as default
        self.layout.addWidget(time_field)
        return time_field

    def populate_table(self, data, headers=None):
        """
        Populate the table with data.

        Parameters:
        - data: List of rows where each row is a list of values for the table.
        - headers: Optional list of column headers. If provided, sets the table headers.
        """
        self.table.setRowCount(0)  # Clear the existing table data

        if headers:
            self.table.setColumnCount(len(headers))  # Set the column count based on headers
            self.table.setHorizontalHeaderLabels(headers)  # Set the headers

        for row_data in data:
            rowPosition = self.table.rowCount()  # Get the current row count
            self.table.insertRow(rowPosition)  # Insert a new row

            # Populate each column in the row with corresponding data
            for col, value in enumerate(row_data):
                self.table.setItem(rowPosition, col, QTableWidgetItem(str(value)))  # Add each cell value as a string

    def generate_report(self, filters, report_type):
        try:
            report_generator = ReportsGenerator()

            # Generate the report using ReportsGenerator
            data = report_generator.generate_report(filters.to_dict(), report_type)

            # Check if data is valid and then populate the report table
            if not data.empty and data is not None:
                self.populate_table(data.values.tolist(),
                                    headers=self.table_headers)
            else:
                QMessageBox.information(self, "No Data", "No report data found for the given filters.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            traceback.print_exc()
