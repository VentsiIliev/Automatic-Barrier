from model.User import User
from repositories.csv_repositories.BaseCSVRepository import BaseCSVRepository
from repositories.csv_repositories.Constants import USER_FIELDS, USER, PASSWORD, EMAIL, ROLE


class CSVUsersRepository(BaseCSVRepository):
    def __init__(self, file_path):
        super().__init__(file_path, USER_FIELDS)

    def get_all(self):
        users = []
        rows = self._read_rows()
        for row in rows:
            # users.append(row)
            user = User(row[USER], row[PASSWORD], row[EMAIL], row[ROLE])
            users.append(user)
        return users

    def get(self, username):
        user = None
        for row in self._read_rows():
            if row[USER] == username:
                user = row
                break
        return user

    def insert(self, user):
        print("inserting user")
        if self.get(user) is None:
            super().insert(**{USER: user.username, PASSWORD: user.password, EMAIL: user.email, ROLE: user.role})

    def delete(self, username):
        super().delete(username)

    def update(self, username, password, email, role):
        rows = self._read_rows()
        for row in rows:
            if row[self.fieldnames[0]] == username:
                row[self.fieldnames[0]] = username
                row[self.fieldnames[1]] = password
                row[self.fieldnames[2]] = email
                row[self.fieldnames[3]] = role
        super().update(rows)
