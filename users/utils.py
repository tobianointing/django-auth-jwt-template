import re


def validate_phone_number(phone_number):
    # Regular expression pattern for a valid phone number
    pattern = r"^(0|\+234)\d{10}$"  # Allowing either 0 or +234 followed by 10 digits

    # Check if the phone number matches the pattern
    if re.match(pattern, phone_number):
        return True
    else:
        return False
