import traceback

from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from API.SingletonDatabase import SingletonDatabase
from control_panel import Validations
from control_panel.BaseLayout import BaseLayout
from control_panel.data_managment.Filter import Filter
from model.User import User


class UserManagementLayout(BaseLayout):
    def __init__(self, parent=None):
        super().__init__("User Management", parent)
        self.initUI()

    def initUI(self):
        """Initialize the user management layout."""
        self.addTable(4, ["Username", "Password", "Role", "Email"])
        self.usernameInput = self.addInputField("Username")
        self.passwordInput = self.addInputField("Password")
        self.roleInput = self.addComboBox(["Select Role", "Manager", "Admin"])
        self.emailInput = self.addInputField("Email")
        self.addButton("Add User", self.addUser)
        self.addButton("Update User", self.updateUser)
        self.addButton("Remove User", self.removeUser)
        self.addButton("Search User", self.searchUser)
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
            QMessageBox.warning(self, "Input Error", "Please enter a valid email.")
            return
        if not Validations.validate_role(role):
            QMessageBox.warning(self, "Input Error", "Please select a role.")
            return
        if not username or not password or not role or not email:
            QMessageBox.warning(self, "Input Error", "Please enter all fields.")
            return

        user = User(username, password, email, role)
        users = SingletonDatabase().getInstance().get_repo('users').get_all()

        if any(u.username == username for u in users):
            QMessageBox.warning(self, "Input Error", "Username already exists.")
            return

        repo = SingletonDatabase().getInstance().get_repo('users')
        repo.insert(user)
        self.loadUsersTable()
        self.clearInputs()

    def updateUser(self):
        selected_row = self.table.currentRow()  # Fixed from `userTable` to `table`
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a user to update.")
            return

        username = self.usernameInput.text()
        password = self.passwordInput.text()
        role = self.roleInput.currentText()
        email = self.emailInput.text()

        if not Validations.validate_email(email):
            QMessageBox.warning(self, "Input Error", "Please enter a valid email.")
            return
        if not Validations.validate_role(role):
            QMessageBox.warning(self, "Input Error", "Please select a role.")
            return
        if not username or not password or not role or not email:
            QMessageBox.warning(self, "Input Error", "Please enter all fields.")
            return

        repo = SingletonDatabase().getInstance().get_repo('users')
        repo.update(username, password, email, role)
        self.loadUsersTable()
        self.clearInputs()

    def removeUser(self):
        selected_row = self.table.currentRow()  # Fixed from `userTable` to `table`
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a user to remove.")
            return

        username = self.table.item(selected_row, 0).text()  # Fixed from `userTable` to `table`
        repo = SingletonDatabase().getInstance().get_repo('users')
        repo.delete(username)
        self.loadUsersTable()

    def create_user_filters(self):
        """Gather user input for filtering and return a Filter object."""
        return Filter(
            username=self.usernameInput.text() or None,
            role=self.roleInput.currentText() if self.roleInput.currentText() != "Select Role" else None,
            email=self.emailInput.text() or None
        )

    def searchUser(self):

        filters = self.create_user_filters()
        self.table.setRowCount(0)  # Clear the user table before populating

        # Load users from the database and filter based on the provided filters
        try:
            users = SingletonDatabase().getInstance().get_repo('users').get_data(filters.to_dict())
        except Exception as e:
            QMessageBox.critical(self, "Error Loading data", f"An error occurred: {str(e)}")
            #print stack trace
            traceback.print_exc()
            return
        try:
            for user in users:
                rowPosition = self.table.rowCount()  # Fixed rowPosition declaration
                self.table.insertRow(rowPosition)
                self.table.setItem(rowPosition, 0, QTableWidgetItem(user.username))
                self.table.setItem(rowPosition, 1,
                                   QTableWidgetItem(user.password))  # Avoid showing passwords in production
                self.table.setItem(rowPosition, 2, QTableWidgetItem(user.role))
                self.table.setItem(rowPosition, 3, QTableWidgetItem(user.email))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


def clearInputs(self):
    """Clear input fields."""
    self.usernameInput.clear()
    self.passwordInput.clear()
    self.emailInput.clear()
    self.roleInput.setCurrentIndex(0)
