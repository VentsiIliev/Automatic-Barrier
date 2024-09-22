import csv

class LoginValidator:
    # Constants
    USERS_CSV_PATH = '../database/users.csv'
    USERNAME_INDEX = 0
    PASSWORD_INDEX = 1

    def validate(self, username, password):
        """
        Validates the username and password.
        Parameters:
            username (str): The username to be validated.
            password (str): The password to be validated.
        Returns:
            bool: True if the username and password are valid, False otherwise.
        """
        try:
            # Read credentials from the CSV file
            with open(self.USERS_CSV_PATH, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)

                # Skip the header row if it exists
                next(reader, None)

                # Iterate through each row and check the username and password
                for row in reader:
                    if len(row) >= 2 and row[self.USERNAME_INDEX] == username and row[self.PASSWORD_INDEX] == password:
                        return True
                return False  # No match found
        except FileNotFoundError:
            print("Error: The 'users.csv' file was not found.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
