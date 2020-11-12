from validate_email import validate_email
from utils.validators.general import validate_fields, validate_fields_types


def validate_create_user(body):
    fields = [
        ('username', str), ('email', str),
        ('full_name', str), ('password', str)
    ]

    required_fields = [f[0] for f in fields]

    wrong_fields = validate_fields(body, required_fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'The following fields are missing: {wrong_fields}'

    wrong_fields = validate_fields_types(body, fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Fields with invalid type: {wrong_fields}'

    wrong_fields = validate_fields_length(body)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Fields with invalid size: {wrong_fields}'

    if not validate_email(body['email']):
        return "Invalid email."

    username_is_invalid = validate_username(body['username'])
    if username_is_invalid:
        return username_is_invalid

    if body['password'].isalpha():
        return "The password has to contain at least one number."

    return None


def validate_update_user(body, params):
    fields = []
    for param in params:
        if param is not 'show_notifications':
            fields.append((param, str))
        else:
            fields.append((param, bool))

    if 'username' in body:
        return 'The username cannot be updated.'

    wrong_fields = validate_fields_types(body, fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Fields with invalid type: {wrong_fields}'

    wrong_fields = validate_fields_length(body)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Fields with invalid size: {wrong_fields}'

    if 'email' in body:
        if not validate_email(body['email']):
            return "Invalid email."

    if 'password' in body:
        if body['password'].isalpha():
            return "The password has to contain at least one number."

    return None


def validate_username(username):
    errors = []
    if username.count(' ') > 0:
        errors.append("The username cannot contain spaces.")

    if not username.isalnum():
        errors.append("The username can only contain letters and numbers.")

    return errors


def validate_fields_length(json):
    errors = []

    if 'username' in json:
        if len(json['username']) < 3 or len(json['username']) > 20:
            errors.append('username')

    if 'email' in json:
        if len(json['email']) < 6 or len(json['email']) > 50:
            errors.append('email')

    if 'password' in json:
        if len(json['password']) < 6 or len(json['password']) > 20:
            errors.append('password')

    if 'full_name' in json:
        if len(json['full_name']) < 1 or len(json['full_name']) > 200:
            errors.append('full_name')

    return errors
