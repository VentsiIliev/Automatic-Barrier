import traceback

from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QLabel, QHBoxLayout

from API.SingletonDatabase import SingletonDatabase
from control_panel import Validations
from control_panel.BaseTableLayout import BaseLayout
from control_panel.data_managment.Filter import Filter
from model.User import User

# Constants for Layout and Table
LAYOUT_TITLE = "User Management"
TABLE_HEADERS = ["User", "Password", "Email", "Role"]
USERNAME_INPUT_FIELD_LABEL = "Username"
PASSWORD_INPUT_FIELD_LABEL = "Password"
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

        roleLabel = QLabel("Role", self)
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

        self.addTable(4, self.table_headers)

        self.loadUsersTable()

    def loadUsersTable(self):
        """Load existing users from the database and populate the user table."""
        self.table.setRowCount(0)
        users = SingletonDatabase().getInstance().get_repo('users').get_all()
        for user in users:
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            self.table.setItem(rowPosition, 0, QTableWidgetItem(user.username))
            self.table.setItem(rowPosition, 1, QTableWidgetItem(user.password))
            self.table.setItem(rowPosition, 2, QTableWidgetItem(user.role))
            self.table.setItem(rowPosition, 3, QTableWidgetItem(user.email))

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
        users = SingletonDatabase().getInstance().get_repo('users').get_all()

        if any(u.username == username for u in users):
            QMessageBox.warning(self, INPUT_ERROR_TITLE, WARNING_MESSAGE_USERNAME_EXISTS)
            return

        try:
            repo = SingletonDatabase().getInstance().get_repo('users')
            repo.insert(user)
        except Exception as e:
            QMessageBox.critical(self, ERROR_TITLE,str(e))
            traceback.print_exc()
        try:
            self.loadUsersTable()
        except Exception as e:
            QMessageBox.critical(self, ERROR_TITLE, str(e))
            traceback.print_exc()
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

        repo = SingletonDatabase().getInstance().get_repo('users')
        repo.update(username, password, email, role)
        self.loadUsersTable()
        self.clearInputs()

    def removeUser(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, SELECTION_ERROR_TITLE, WARNING_MESSAGE_SELECT_USER_TO_REMOVE)
            return

        username = self.table.item(selected_row, 0).text()
        repo = SingletonDatabase().getInstance().get_repo('users')
        repo.delete(username)
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
        super().generate_report(filters, report_type="user")

    def clearInputs(self):
        """Clear input fields."""
        self.usernameInput.clear()
        self.passwordInput.clear()
        self.emailInput.clear()
        self.roleInput.setCurrentIndex(0)
