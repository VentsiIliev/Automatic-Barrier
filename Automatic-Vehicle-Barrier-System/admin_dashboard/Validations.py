import re


def validate_email(email):
    if email == "" or email == "Enter your email":
        return False
    # check with regex pattern
    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    if re.match(pattern, email):
        return True
    else:
        return False

def validate_role(role):
    if role == "Select Role":
        return False
    return True
