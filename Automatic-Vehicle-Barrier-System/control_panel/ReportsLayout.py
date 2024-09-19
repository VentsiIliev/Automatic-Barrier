from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, \
    QLineEdit, QComboBox, QPushButton, QMessageBox


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
        self.dateInput = QLineEdit(self)
        self.dateInput.setPlaceholderText("Date (YYYY-MM-DD)")
        filterLayout.addWidget(self.dateInput)

        # Time Filter
        self.timeInput = QLineEdit(self)
        self.timeInput.setPlaceholderText("Time (HH:MM)")
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
        """Generate a report based on the filter criteria."""
        reg = self.registrationInput.text().upper()
        date = self.dateInput.text()
        time = self.timeInput.text()
        direction = self.directionInput.currentText()
        access_level = self.accessLevelInput.currentText()
        access_status = self.accessStatusInput.currentText()

        # For now, populate with some placeholder data
        data = [
            (reg or "XYZ123", date, time, direction or "IN", access_level or "User", access_status or "GRANTED")
        ]

        self.reportTable.setRowCount(len(data))

        for row, (reg, date, time, direction, access_level, status) in enumerate(data):
            self.reportTable.setItem(row, 0, QTableWidgetItem(reg))
            self.reportTable.setItem(row, 1, QTableWidgetItem(date))
            self.reportTable.setItem(row, 2, QTableWidgetItem(time))
            self.reportTable.setItem(row, 3, QTableWidgetItem(direction))
            self.reportTable.setItem(row, 4, QTableWidgetItem(access_level))
            self.reportTable.setItem(row, 5, QTableWidgetItem(status))
