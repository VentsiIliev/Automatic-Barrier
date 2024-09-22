from PyQt5.QtWidgets import QHBoxLayout, QLabel

from control_panel.BaseTableLayout import BaseLayout
from control_panel.data_managment.Filter import Filter

LAYOUT_TITLE = "Reports"
TABLE_HEADERS = ["Access Status", "Date", "Time", "Registration", "Direction", "Owner"]
REGISTRATION_INPUT_FIELD_LABEL = "Registration Number"
FROM_DATE_INPUT_FIELD_LABEL = "From Date"
TO_DATE_INPUT_FIELD_LABEL = "To Date"
FROM_TIME_INPUT_FIELD_LABEL = "From Time"
TO_TIME_INPUT_FIELD_LABEL = "To Time"
DIRECTION_INPUT_FIELD_LABELS = ["All", "IN", "OUT"]
ACCESS_LEVEL_INPUT_FIELD_LABELS = ["All", "Admin", "User", "Guest"]
ACCESS_STATUS_INPUT_FIELD_LABELS = ["All", "GRANTED", "DENIED"]
GENERATE_REPORT_BUTTON_LABEL = "Generate Report"

class ReportsLayout(BaseLayout):
    def __init__(self, parent=None):
        self.table_headers = TABLE_HEADERS
        super().__init__(LAYOUT_TITLE, self.table_headers, parent)
        self.initUI()

    def initUI(self):
        """Initialize the reports' layout."""
        # Add input fields (filters)
        self.registrationInput = self.addInputField(REGISTRATION_INPUT_FIELD_LABEL)

        # Create a horizontal layout for date
        dateLayout = QHBoxLayout()

        # Add 'From Date' and 'To Date' fields to the horizontal layout
        fromDateLabel = QLabel(FROM_DATE_INPUT_FIELD_LABEL, self)
        dateLayout.addWidget(fromDateLabel)
        self.fromDateInput = self.addDateField(FROM_DATE_INPUT_FIELD_LABEL)
        dateLayout.addWidget(self.fromDateInput)

        toDateLabel = QLabel(TO_DATE_INPUT_FIELD_LABEL, self)
        dateLayout.addWidget(toDateLabel)
        self.toDateInput = self.addDateField(TO_DATE_INPUT_FIELD_LABEL)
        dateLayout.addWidget(self.toDateInput)

        # Add the horizontal layout to the main layout
        self.layout.addLayout(dateLayout)

        # Create a horizontal layout for time
        timeLayout = QHBoxLayout()

        # Add 'From Time' and 'To Time' fields to the horizontal layout
        fromTimeLabel = QLabel(FROM_TIME_INPUT_FIELD_LABEL, self)
        timeLayout.addWidget(fromTimeLabel)
        self.timeFromInput = self.addTimeField(FROM_TIME_INPUT_FIELD_LABEL)
        timeLayout.addWidget(self.timeFromInput)

        toTimeLabel = QLabel(TO_TIME_INPUT_FIELD_LABEL, self)
        timeLayout.addWidget(toTimeLabel)
        self.timeToInput = self.addTimeField(TO_TIME_INPUT_FIELD_LABEL)
        timeLayout.addWidget(self.timeToInput)

        # Add the horizontal layout to the main layout
        self.layout.addLayout(timeLayout)

        # Create a horizontal layout for other filters
        otherFiltersLayout = QHBoxLayout()

        # Add 'Direction', 'Access Level', and 'Access Status' fields to the horizontal layout
        directionLabel = QLabel("Direction", self)
        otherFiltersLayout.addWidget(directionLabel)
        self.directionInput = self.addComboBox(DIRECTION_INPUT_FIELD_LABELS)
        otherFiltersLayout.addWidget(self.directionInput)

        accessLevelLabel = QLabel("Access Level", self)
        otherFiltersLayout.addWidget(accessLevelLabel)
        self.accessLevelInput = self.addComboBox(ACCESS_LEVEL_INPUT_FIELD_LABELS)
        otherFiltersLayout.addWidget(self.accessLevelInput)

        accessStatusLabel = QLabel("Access Status", self)
        otherFiltersLayout.addWidget(accessStatusLabel)
        self.accessStatusInput = self.addComboBox(ACCESS_STATUS_INPUT_FIELD_LABELS)
        otherFiltersLayout.addWidget(self.accessStatusInput)

        # Add the horizontal layout to the main layout
        self.layout.addLayout(otherFiltersLayout)

        # Add Generate Report Button
        self.addButton(GENERATE_REPORT_BUTTON_LABEL, self.get_report)

        # Add Report Table
        self.addTable(6, self.table_headers)

    def create_filters(self):
        """Gather filter input from the UI and return a dictionary."""
        filters = Filter(
            registration_number=self.registrationInput.text().upper() or None,

            # Correctly include both 'from' and 'to' dates in the date range tuple
            date_range=(
                self.fromDateInput.date().toString("yyyy-MM-dd"), self.toDateInput.date().toString("yyyy-MM-dd"))
            if self.fromDateInput.date() and self.toDateInput.date() else None,

            # Include both 'from' and 'to' times in the time range tuple
            time_range=(self.timeFromInput.time().toString("hh:mm:ss"), self.timeToInput.time().toString("hh:mm:ss"))
            if self.timeFromInput.time() and self.timeToInput.time() else None,

            # Only include direction if it's not "All"
            direction=self.directionInput.currentText() if self.directionInput.currentText() != "All" else None,

            # Only include access status if it's not "All"
            access_status=self.accessStatusInput.currentText() if self.accessStatusInput.currentText() != "All" else None
        )

        return filters

    def get_report(self):
        filters = self.create_filters()
        super().generate_report(filters)
