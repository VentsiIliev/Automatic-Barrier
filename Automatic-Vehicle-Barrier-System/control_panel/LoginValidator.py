import csv


class LoginValidator:

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
            with open('credentials.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)

                # Skip the header row if it exists
                next(reader, None)

                # Iterate through each row and check the username and password
                for row in reader:
                    if len(row) >= 2 and row[0] == username and row[1] == password:
                        return True
                return False  # No match found
        except FileNotFoundError:
            print("Error: The 'credentials.csv' file was not found.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False