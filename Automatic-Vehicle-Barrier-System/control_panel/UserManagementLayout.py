from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from API.SingletonDatabase import SingletonDatabase
from model.User import User


class UserManagementLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        titleLabel = QLabel("User Management", self)
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(titleLabel)

        # User Input Fields
        self.usernameInput = QLineEdit(self)
        self.usernameInput.setPlaceholderText("Username")
        layout.addWidget(self.usernameInput)

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setPlaceholderText("Password")
        self.passwordInput.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passwordInput)

        # Buttons for Add, Update, Remove, Search
        buttonLayout = QVBoxLayout()

        addUserButton = QPushButton("Add User", self)
        addUserButton.clicked.connect(self.addUser)
        buttonLayout.addWidget(addUserButton)

        updateUserButton = QPushButton("Update User", self)
        updateUserButton.clicked.connect(self.updateUser)
        buttonLayout.addWidget(updateUserButton)

        removeUserButton = QPushButton("Remove User", self)
        removeUserButton.clicked.connect(self.removeUser)
        buttonLayout.addWidget(removeUserButton)

        searchUserButton = QPushButton("Search User", self)
        searchUserButton.clicked.connect(self.searchUser)
        buttonLayout.addWidget(searchUserButton)

        layout.addLayout(buttonLayout)

        # User Table
        self.userTable = QTableWidget(self)
        self.userTable.setColumnCount(2)
        self.userTable.setHorizontalHeaderLabels(["Username", "Password"])
        self.userTable.cellDoubleClicked.connect(self.loadUserData)  # Load user data on double click
        layout.addWidget(self.userTable)

        self.loadUsersTable()

        self.setLayout(layout)

    def loadUsersTable(self):
        """Load existing users from the database and populate the user table."""
        self.userTable.setRowCount(0)  # Clear existing rows
        users = SingletonDatabase().getInstance().get_repo('users').get_all()
        for user in users:
            rowPosition = self.userTable.rowCount()
            self.userTable.insertRow(rowPosition)
            self.userTable.setItem(rowPosition, 0, QTableWidgetItem(user.username))
            self.userTable.setItem(rowPosition, 1, QTableWidgetItem(user.password))  # Avoid showing passwords in production

    def addUser(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        if username and password:
            user = User(username, password, "N/A", "N/A")
            users = SingletonDatabase().getInstance().get_repo('users').get_all()

            if any(u.username == username for u in users):
                QMessageBox.warning(self, "Input Error", "Username already exists.")
                return

            db = SingletonDatabase().getInstance()
            repo = db.get_repo('users')
            repo.insert(user)

            self.loadUsersTable()  # Reload the user table
            self.usernameInput.clear()
            self.passwordInput.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")

    def updateUser(self):
        selected_row = self.userTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a user to update.")
            return

        username = self.usernameInput.text()
        password = self.passwordInput.text()

        if username and password:
            user = User(username, password, "N/A", "N/A")
            db = SingletonDatabase().getInstance()
            repo = db.get_repo('users')
            repo.update(user)  # Assume the update method exists

            self.loadUsersTable()  # Reload the user table
            self.usernameInput.clear()
            self.passwordInput.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")

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
                    self.userTable.setItem(rowPosition, 1, QTableWidgetItem(user.password))  # Avoid showing passwords in production
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a username to search.")

    def loadUserData(self, row, column):
        """Load user data into input fields for editing."""
        username = self.userTable.item(row, 0).text()
        password = self.userTable.item(row, 1).text()
        self.usernameInput.setText(username)
        self.passwordInput.setText(password)
