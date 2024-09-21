from model.User import User
from repositories.csv_repositories.BaseCSVRepository import BaseCSVRepository
from repositories.csv_repositories.Constants import USER_FIELDS, USER, PASSWORD, EMAIL, ROLE


class CSVUsersRepository(BaseCSVRepository):
    def __init__(self, file_path):
        super().__init__(file_path, USER_FIELDS)

    def get_all(self):
        users = []
        df = self._read_rows()

        if df.empty:
            print("No users found in the CSV.")
            return users

        for _, row in df.iterrows():
            # Access row data using the column names directly
            user = User(
                username=row[USER],
                password=row[PASSWORD],
                email=row[EMAIL],
                role=row[ROLE]
            )
            users.append(user)

        return users

    def get(self, username):
        for row in self._read_rows():
            if row[USER] == username:
                return row
        return None

    def insert(self, user):
        print("Inserting user")
        if self.get(user.username) is None:  # Check by username
            super().insert(**{USER: user.username, PASSWORD: user.password, EMAIL: user.email, ROLE: user.role})

    def delete(self, username):
        super().delete(username)

    def update(self, rows):
        """Update users with the provided list of user data."""
        print("Updating users")
        current_rows = self._read_rows()
        for row in current_rows:
            for updated_user in rows:
                if row[USER] == updated_user[USER]:  # Ensure matching on username
                    row[PASSWORD] = updated_user[PASSWORD]
                    row[EMAIL] = updated_user[EMAIL]
                    row[ROLE] = updated_user[ROLE]
        super().update(current_rows)

    def get_data(self, filters=None):
        users = []
        data = super().get_data(filters)

        # Skip the first row (header) using .iloc
        for index, row in data.iloc[1:].iterrows():  # Start from the second row
            print("row", row)
            user = User(
                username=row[USER],
                password=row[PASSWORD],
                email=row[EMAIL],
                role=row[ROLE]
            )
            users.append(user)

        return users

