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

        # Add 'From Date' and 'To Date' fields
        self.fromDateInput = self.addDateField(FROM_DATE_INPUT_FIELD_LABEL)
        self.toDateInput = self.addDateField(TO_DATE_INPUT_FIELD_LABEL)

        # Add 'From Time' and 'To Time' fields
        self.timeFromInput = self.addTimeField(FROM_TIME_INPUT_FIELD_LABEL)
        self.timeToInput = self.addTimeField(TO_TIME_INPUT_FIELD_LABEL)

        # Other filters
        self.directionInput = self.addComboBox(DIRECTION_INPUT_FIELD_LABELS)
        self.accessLevelInput = self.addComboBox(ACCESS_LEVEL_INPUT_FIELD_LABELS)
        self.accessStatusInput = self.addComboBox(ACCESS_STATUS_INPUT_FIELD_LABELS)

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
