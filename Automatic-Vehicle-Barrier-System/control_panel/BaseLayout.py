from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QPushButton, QLineEdit, QComboBox

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
