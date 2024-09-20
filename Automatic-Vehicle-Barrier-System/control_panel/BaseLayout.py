from PyQt5.QtCore import QTime, QDate
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QPushButton, QLineEdit, QComboBox, QDateEdit, \
    QTimeEdit


class BaseLayout(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
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
