class User:
    def __init__(self, username, password, email, role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def __str__(self):
        return f"User: {self.username}, Email: {self.email}, Role: {self.role}"