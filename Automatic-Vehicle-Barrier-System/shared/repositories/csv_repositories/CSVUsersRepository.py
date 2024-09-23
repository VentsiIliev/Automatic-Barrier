import traceback

from admin_dashboard.model.User import User
from shared.repositories.csv_repositories.BaseCSVRepository import BaseCSVRepository
from shared.repositories.csv_repositories.Constants import USER_FIELDS, USER, PASSWORD, EMAIL, ROLE


class CSVUsersRepository(BaseCSVRepository):
    def __init__(self, file_path):
        super().__init__(file_path, USER_FIELDS)

    def get_all(self):
        users = []
        df = self._read_rows()

        if df.empty:
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
        df = self._read_rows()
        row = df[df[USER] == username]  # Use lowercase 'User'
        # Iterate over the rows of the DataFrame
        if not row.empty:
            row = row.iloc[0]
            return User(row[USER].values[0], row[PASSWORD].values[0], row[EMAIL].values[0], row[ROLE].values[0])

        return None  # Return None if user is not found

    def insert(self, user):
        try:
            if self.get(user.username) is None:  # Check by username
                super().insert(**{USER: user.username, PASSWORD: user.password, EMAIL: user.email, ROLE: user.role})
        except Exception as e:
            traceback.print_exc()

    def delete(self, username):
        super().delete(username)

    def update(self, rows):
        """Update users with the provided list of user data."""
        current_rows = self._read_rows()
        for row in current_rows:
            for updated_user in rows:
                if row[USER] == updated_user[USER]:  # Ensure matching on username
                    row[PASSWORD] = updated_user[PASSWORD]
                    row[EMAIL] = updated_user[EMAIL]
                    row[ROLE] = updated_user[ROLE]
        super().update(current_rows)

    def get_data(self, filters=None):
        """Retrieve filtered data based on given criteria."""
        return super().get_data(filters)
