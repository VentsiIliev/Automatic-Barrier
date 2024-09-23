import traceback

from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QLabel, QHBoxLayout

from shared.CSVFileName import CSVFileName
from shared.SingletonDatabase import SingletonDatabase
from admin_dashboard import Validations
from admin_dashboard.settings import Settings
from admin_dashboard.data_managment.ReportType import ReportType
from admin_dashboard.view.BaseTableLayout import BaseLayout
from admin_dashboard.data_managment.Filter import Filter
from admin_dashboard.model.User import User

# Constants for Layout and Table
LAYOUT_TITLE = "User Management"
CSV_FILE = CSVFileName.USERS.strip_extension()
TABLE_HEADERS = ["User", "Password", "Email", "Role"]
USERNAME_INPUT_FIELD_LABEL = "Username"
PASSWORD_INPUT_FIELD_LABEL = "Password"

ROLE_INPUT_FIELD_LABEL = "Role"
ROLE_INPUT_FIELD_LABELS = ["Select Role", "Manager", "Admin"]

EMAIL_INPUT_FIELD_LABEL = "Email"
ADD_USER_BUTTON_LABEL = "Add User"
UPDATE_USER_BUTTON_LABEL = "Update User"
REMOVE_USER_BUTTON_LABEL = "Remove User"
SEARCH_USER_BUTTON_LABEL = "Search User"


# Warning Messages
WARNING_MESSAGE_SELECT_USER_TO_UPDATE = "Please select a user to update."
WARNING_MESSAGE_SELECT_USER_TO_REMOVE = "Please select a user to remove."
WARNING_MESSAGE_USERNAME_EXISTS = "Username already exists."
WARNING_MESSAGE_ENTER_ALL_FIELDS = "Please enter all fields."
WARNING_MESSAGE_INVALID_EMAIL = "Please enter a valid email."
WARNING_MESSAGE_PLEASE_SELECT_ROLE = "Please select a role."
INPUT_ERROR_TITLE = "Input Error"
SELECTION_ERROR_TITLE = "Selection Error"
ERROR_TITLE = "Error"




class UserManagementLayout(BaseLayout):
    def __init__(self, parent=None):
        self.table_headers = TABLE_HEADERS
        super().__init__(LAYOUT_TITLE, self.table_headers, parent)
        self.initUI()

    def initUI(self):
        """Initialize the user management layout."""
        # Create a horizontal layout for user details
        userDetailsLayout = QHBoxLayout()

        # Add 'Username', 'Password', 'Role', and 'Email' fields to the horizontal layout
        usernameLabel = QLabel(USERNAME_INPUT_FIELD_LABEL, self)
        userDetailsLayout.addWidget(usernameLabel)
        self.usernameInput = self.addInputField(USERNAME_INPUT_FIELD_LABEL)
        userDetailsLayout.addWidget(self.usernameInput)

        passwordLabel = QLabel(PASSWORD_INPUT_FIELD_LABEL, self)
        userDetailsLayout.addWidget(passwordLabel)
        self.passwordInput = self.addInputField(PASSWORD_INPUT_FIELD_LABEL)
        userDetailsLayout.addWidget(self.passwordInput)

        roleLabel = QLabel(ROLE_INPUT_FIELD_LABEL, self)
        userDetailsLayout.addWidget(roleLabel)
        self.roleInput = self.addComboBox(ROLE_INPUT_FIELD_LABELS)
        userDetailsLayout.addWidget(self.roleInput)

        emailLabel = QLabel(EMAIL_INPUT_FIELD_LABEL, self)
        userDetailsLayout.addWidget(emailLabel)
        self.emailInput = self.addInputField(EMAIL_INPUT_FIELD_LABEL)
        userDetailsLayout.addWidget(self.emailInput)

        # Add the horizontal layout to the main layout
        self.layout.addLayout(userDetailsLayout)

        # Create a horizontal layout for buttons
        buttonsLayout = QHBoxLayout()

        # Add buttons to the horizontal layout
        buttonsLayout.addWidget(self.addButton(ADD_USER_BUTTON_LABEL, self.addUser))
        buttonsLayout.addWidget(self.addButton(UPDATE_USER_BUTTON_LABEL, self.updateUser))
        buttonsLayout.addWidget(self.addButton(REMOVE_USER_BUTTON_LABEL, self.removeUser))
        buttonsLayout.addWidget(self.addButton(SEARCH_USER_BUTTON_LABEL, self.search_users))

        # Add the horizontal layout to the main layout
        self.layout.addLayout(buttonsLayout)

        # Add table to the layout
        self.addTable(4, self.table_headers)

        # Connect row selection to the handler
        self.table.itemSelectionChanged.connect(self.on_user_selected)

        # Load users into the table
        self.loadUsersTable()

    def loadUsersTable(self):
        """Load existing users from the database and populate the user table."""
        self.table.setRowCount(0)
        users = SingletonDatabase().getInstance().get_repo(CSV_FILE).get_all()
        for user in users:
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            self.table.setItem(rowPosition, 0, QTableWidgetItem(user.username))
            self.table.setItem(rowPosition, 1, QTableWidgetItem(user.password))
            self.table.setItem(rowPosition, 2, QTableWidgetItem(user.role))
            self.table.setItem(rowPosition, 3, QTableWidgetItem(user.email))

    def on_user_selected(self):
        """Handle user selection from the table and populate the input fields."""
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            # Populate the input fields with the selected user data
            self.usernameInput.setText(self.table.item(selected_row, 0).text())  # Username
            self.passwordInput.setText(self.table.item(selected_row, 1).text())  # Password
            self.roleInput.setCurrentText(self.table.item(selected_row, 2).text())  # Role
            self.emailInput.setText(self.table.item(selected_row, 3).text())  # Email
        else:
            # Clear the input fields if no user is selected
            self.clearInputs()

    def addUser(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        role = self.roleInput.currentText()
        email = self.emailInput.text()

        if not Validations.validate_email(email):
            QMessageBox.warning(self, INPUT_ERROR_TITLE, WARNING_MESSAGE_INVALID_EMAIL)
            return
        if not Validations.validate_role(role):
            QMessageBox.warning(self, INPUT_ERROR_TITLE, WARNING_MESSAGE_PLEASE_SELECT_ROLE)
            return
        if not username or not password or not role or not email:
            QMessageBox.warning(self, INPUT_ERROR_TITLE, WARNING_MESSAGE_ENTER_ALL_FIELDS)
            return

        user = User(username, password, email, role)
        users = SingletonDatabase().getInstance().get_repo(CSV_FILE).get_all()

        if any(u.username == username for u in users):
            QMessageBox.warning(self, INPUT_ERROR_TITLE, WARNING_MESSAGE_USERNAME_EXISTS)
            return

        try:
            repo = SingletonDatabase().getInstance().get_repo(CSV_FILE)
            repo.insert(user)
        except Exception as e:
            QMessageBox.critical(self, ERROR_TITLE, str(e))
            traceback.print_exc()

        self.loadUsersTable()
        self.clearInputs()

    def updateUser(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, SELECTION_ERROR_TITLE, WARNING_MESSAGE_SELECT_USER_TO_UPDATE)
            return

        username = self.usernameInput.text()
        password = self.passwordInput.text()
        role = self.roleInput.currentText()
        email = self.emailInput.text()

        if not Validations.validate_email(email):
            QMessageBox.warning(self, INPUT_ERROR_TITLE, WARNING_MESSAGE_INVALID_EMAIL)
            return
        if not Validations.validate_role(role):
            QMessageBox.warning(self, INPUT_ERROR_TITLE, WARNING_MESSAGE_PLEASE_SELECT_ROLE)
            return
        if not username or not password or not role or not email:
            QMessageBox.warning(self, INPUT_ERROR_TITLE, WARNING_MESSAGE_ENTER_ALL_FIELDS)
            return

        try:
            repo = SingletonDatabase().getInstance().get_repo(CSV_FILE)
            repo.update(username, password, email, role)
        except Exception as e:
            QMessageBox.critical(self, ERROR_TITLE, str(e))
            traceback.print_exc()

        self.loadUsersTable()
        self.clearInputs()

    def removeUser(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, SELECTION_ERROR_TITLE, WARNING_MESSAGE_SELECT_USER_TO_REMOVE)
            return

        username = self.table.item(selected_row, 0).text()
        try:
            repo = SingletonDatabase().getInstance().get_repo(CSV_FILE)
            repo.delete(username)
        except Exception as e:
            QMessageBox.critical(self, ERROR_TITLE, str(e))
            traceback.print_exc()

        self.loadUsersTable()

    def create_user_filters(self):
        """Gather user input for filtering and return a Filter object."""
        return Filter(
            username=self.usernameInput.text() or None,
            role=self.roleInput.currentText() if self.roleInput.currentText() != ROLE_INPUT_FIELD_LABELS[0] else None,
            email=self.emailInput.text() or None
        )

    def search_users(self):
        filters = self.create_user_filters()
        super().generate_report(filters, ReportType.USER)

    def clearInputs(self):
        """Clear input fields."""
        self.usernameInput.clear()
        self.passwordInput.clear()
        self.emailInput.clear()
        self.roleInput.setCurrentIndex(0)
