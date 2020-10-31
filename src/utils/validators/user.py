from validate_email import validate_email
from utils.validators.general import validate_fields, validate_fields_types


def validate_create_user(body):
    fields = [
        ('username', str), ('email', str),
        ('full_name', str), ('password', str)
    ]

    required_fields = [f[0] for f in fields]
    error = None

    wrong_fields = validate_fields(body, required_fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        error = f'Os seguintes campos estão faltando: {wrong_fields}'

    wrong_fields = validate_fields_types(body, fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        error = f'Campos com tipo inválido: {wrong_fields}'

    wrong_fields = validate_fields_length(body)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        error = f'Campos com tamanho inválido: {wrong_fields}'

    if not validate_email(body['email']):
        error = "Email inválido"

    username_is_invalid = validate_username(body['username'])
    if username_is_invalid:
        error = username_is_invalid

    if body['password'].isalpha():
        error = "A senha deve conter pelo menos um número."

    return error


def validate_update_user(body, params):
    error = None
    fields = []
    for param in params:
        fields.append((param, str))

    if 'username' in body:
        error = 'Username não pode ser atualizado.'

    wrong_fields = validate_fields_types(body, fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        error = f'Campos com tipo inválido: {wrong_fields}'

    wrong_fields = validate_fields_length(body)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        error = f'Campos com tamanho inválido: {wrong_fields}'

    if 'email' in body:
        if not validate_email(body['email']):
            error = "Email inválido"

    if 'password' in body:
        if body['password'].isalpha():
            error = "A senha deve conter pelo menos um número."

    return error


def validate_username(username):
    errors = []
    if username.count(' ') > 0:
        errors.append("O username não pode conter espaços.")

    if not username.isalnum():
        errors.append("O username pode conter apenas letras e números.")

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
