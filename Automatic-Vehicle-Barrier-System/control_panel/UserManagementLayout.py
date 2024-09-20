from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from API.SingletonDatabase import SingletonDatabase
from control_panel import Validations
from control_panel.BaseLayout import BaseLayout
from model.User import User


class UserManagementLayout(BaseLayout):
    def __init__(self, parent=None):
        super().__init__("User Management", parent)
        self.initUI()

    def initUI(self):
        """Initialize the user management layout."""

        # Add User Table
        self.addTable(4, ["Username", "Password", "Role", "Email"])

        # Add input fields
        self.usernameInput = self.addInputField("Username")
        self.passwordInput = self.addInputField("Password")
        self.roleInput = self.addComboBox(["Select Role", "Manager", "Admin"])
        self.emailInput = self.addInputField("Email")

        # Add Buttons
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

        # username, password, role, email = self.validateFields()
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        role = self.roleInput.currentText()  # Get selected role
        email = self.emailInput.text()

        if not Validations.validate_email(email):
            QMessageBox.warning(self, "Input Error", "Please enter your email.")
            return
        if not Validations.validate_role(role):
            QMessageBox.warning(self, "Input Error", "Please select a role.")
            return

        if not username or not password or not role or not email:
            QMessageBox.warning(self, "Input Error", "Please enter all fields.")

        user = User(username, password, email, role, )  # Assume User has a role parameter
        users = SingletonDatabase().getInstance().get_repo('users').get_all()

        if any(u.username == username for u in users):
            QMessageBox.warning(self, "Input Error", "Username already exists.")
            return

        db = SingletonDatabase().getInstance()
        repo = db.get_repo('users')
        repo.insert(user)

        self.loadUsersTable()  # Reload the user table
        self.clearInputs()

    def updateUser(self):
        selected_row = self.userTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a user to update.")
            return

        # username, password, role, email = self.validateFields()
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        role = self.roleInput.currentText()  # Get selected role
        email = self.emailInput.text()

        if not Validations.validate_email(email):
            QMessageBox.warning(self, "Input Error", "Please enter your email.")
            return
        if not Validations.validate_role(role):
            QMessageBox.warning(self, "Input Error", "Please select a role.")
            return

        if not username or not password or not role or not email:
            QMessageBox.warning(self, "Input Error", "Please enter all fields.")

        user = User(username, password, email, role)  # Assume User has a role parameter
        db = SingletonDatabase().getInstance()
        repo = db.get_repo('users')
        # repo.update(user)  # Assume the update method exists
        repo.update(username, password, email, role)
        self.loadUsersTable()  # Reload the user table
        self.clearInputs()

    def removeUser(self):
        selected_row = self.userTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a user to remove.")
            return

        username = self.userTable.item(selected_row, 0).text()
        db = SingletonDatabase().getInstance()
        repo = db.get_repo('users')
        repo.delete(username)  # Assume the remove method exists

        self.loadUsersTable()  # Reload the user table

    def searchUser(self):
        search_username = self.usernameInput.text()
        if search_username:
            self.userTable.setRowCount(0)  # Clear existing rows
            users = SingletonDatabase().getInstance().get_repo('users').get_all()

            for user in users:
                if search_username.lower() in user.username.lower():
                    rowPosition = self.userTable.rowCount()
                    self.userTable.insertRow(rowPosition)
                    self.userTable.setItem(rowPosition, 0, QTableWidgetItem(user.username))
                    self.userTable.setItem(rowPosition, 1,
                                           QTableWidgetItem(user.password))  # Avoid showing passwords in production
                    self.userTable.setItem(rowPosition, 2,
                                           QTableWidgetItem(user.role))  # Assuming user has a role attribute
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a username to search.")
    def clearInputs(self):
        """Clear input fields."""
        self.usernameInput.clear()
        self.passwordInput.clear()
        self.emailInput.clear()
        self.roleInput.setCurrentIndex(0)
