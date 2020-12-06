from functools import wraps
from flask import request
import jwt

from settings import SECRET_KEY
from utils.formatters import create_response
from controllers import user


def validate_fields(json, fields):
    '''Validates if the json has the right attributes
    To verify a dict inside a dict, separate the keys with /
    Ex: validate_fields({'msg': {'content':'Hello World'}}, 'msg/content')

    Parameters:
        - JSON to be validated-> dict
        - fields to be verified -> *str

    Return:
        - Lists attributes not found or empty list
    '''

    try:
        errors = []
        for field in fields:
            f = field.split('/')
            f = list(filter(None, f))
            if len(f) == 1:
                if f[0] not in json:
                    errors.append(f[0])
            else:
                if f[0] in json:
                    err = validate_fields(json[f[0]], '/'.join(f[1:]))
                    if err:
                        errors.append(err[0])
                else:
                    errors.append(f[0])
        return errors
    except Exception:
        return ['Invalid JSON']


def validate_fields_types(json, params):
    '''Validates the fields types in a JSON

    Parameters:
        - JSON
        - params -> tuple list composed by a field and a value

    Return:
        - Lists attributes not found or empty list
    '''
    errors = []
    for field, value_type in params:
        if not isinstance(json.get(field), value_type):
            errors.append(field)
    return errors


def validate_header(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        type_error = ('Provide a Json', 415)
        header_values = ['*/*', 'application/json']
        header_keys = ['Accept', 'Content-Type']
        header = request.headers
        rm = request.method
        methods = ['POST', 'PUT', 'PATCH']
        if rm in methods:
            if not request.data:
                return create_response(*type_error)
            if not all(h in header for h in header_keys):
                return create_response(*type_error)
            if not all(header[h] in header_values for h in header_keys):
                return create_response(*type_error)

        return func(*args, **kwargs)

    return decorated_function


def validate_token(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth = request.headers.get('Authorization')

        if not auth:
            return 'Provide a valid authorization', 403

        try:
            username = jwt.decode(
                    auth, SECRET_KEY, algorithms=['HS256']
            )['username']
            result, code = user.get_one_user(username)
            if code == 200:
                return func(username, *args, **kwargs)
            if code == 404:
                return "Usuário não existe", code
            return result, code
        except jwt.InvalidTokenError:
            return 'Invalid token', 401

    return decorated_function
