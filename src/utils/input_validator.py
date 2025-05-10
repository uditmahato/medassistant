def validate_non_empty_string(value):
    return isinstance(value, str) and value.strip() != ""

def validate_age(age_str):
    try:
        age = int(age_str)
        return 0 <= age <= 120
    except ValueError:
        return False