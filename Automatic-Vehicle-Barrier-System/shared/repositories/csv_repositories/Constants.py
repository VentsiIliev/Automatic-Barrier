# Constants.py
# Constants for the CSV repositories.

# Access Denied Repository Fields
EVENT_TYPE = 'Event Type'
DATE = 'Date'
TIME = 'Time'
REGISTRATION_NUMBER = 'Registration Number'
DIRECTION = 'Direction'
OWNER = 'Owner'
ACCESS_LEVEL = 'Access Level'
USER = 'User'
PASSWORD = 'Password'
EMAIL = 'Email'
ROLE = 'Role'

# Access Denied Repository Fields
ACCESS_DENIED_FIELDS = [EVENT_TYPE, DATE, TIME, REGISTRATION_NUMBER, DIRECTION, OWNER]

# Access Granted Repository Fields
ACCESS_GRANTED_FIELDS = [EVENT_TYPE, DATE, TIME, REGISTRATION_NUMBER, DIRECTION, OWNER]

# Vehicles On Premises Repository Fields
VEHICLES_ON_PREMISES_FIELDS = [REGISTRATION_NUMBER]

# Whitelisted Vehicles Repository Fields
WHITELISTED_VEHICLES_FIELDS = [REGISTRATION_NUMBER, OWNER, ACCESS_LEVEL]

# User Repository Fields
USER_FIELDS = [USER, PASSWORD, EMAIL, ROLE]
