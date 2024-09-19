from PyQt5.QtWidgets import (QVBoxLayout, QPushButton,
                             QLabel, QLineEdit, QDialog, QMessageBox)


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setWindowTitle("Login")

        self.layout = QVBoxLayout(self)

        self.usernameLabel = QLabel("Username:")
        self.usernameInput = QLineEdit(self)

        self.passwordLabel = QLabel("Password:")
        self.passwordInput = QLineEdit(self)
        self.passwordInput.setEchoMode(QLineEdit.Password)

        self.loginButton = QPushButton("Login", self)
        self.loginButton.clicked.connect(self.login)

        self.layout.addWidget(self.usernameLabel)
        self.layout.addWidget(self.usernameInput)
        self.layout.addWidget(self.passwordLabel)
        self.layout.addWidget(self.passwordInput)
        self.layout.addWidget(self.loginButton)

        self.setLayout(self.layout)
        self.valid_users = {
            'admin': 'admin123',
            'user': 'user123',
            'guest': 'guest123'
        }

        self.logged_in_user = None

    def login(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        if username in self.valid_users and self.valid_users[username] == password:
            self.logged_in_user = username
            self.accept()  # Close the dialog and signal success
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')

    def get_logged_in_user(self):
        return self.logged_in_user