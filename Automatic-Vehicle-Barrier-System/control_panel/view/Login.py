from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from control_panel.LoginValidator import LoginValidator

class LoginLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.username_label = QLabel("Username", self)
        self.layout.addWidget(self.username_label)
        self.username_entry = QLineEdit(self)
        self.layout.addWidget(self.username_entry)

        self.password_label = QLabel("Password", self)
        self.layout.addWidget(self.password_label)
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_entry)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        loginValidator = LoginValidator()
        if loginValidator.validate(username, password):
            print('Login successful')
            self.parent().admin_panel.show()
            #hide the login layout
            self.hide()
        else:
            print('Invalid username or password')

    def resizeEvent(self, event):
        # Adjust the size of the LoginLayout to match the new size of its parent widget
        self.resize(self.parent().size())
        super().resizeEvent(event)