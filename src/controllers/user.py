from database.models import User
from database import db
from utils.formatters import get_row_dict
from utils.validators.user import validate_create_user, validate_update_user


def create_user(body):

    errors = validate_create_user(body)
    if errors:
        return errors, 400

    user = User(
        body['username'],
        body['email'],
        body['password'],
        body['full_name']
    )
    result, code = db.insert_one(user)

    return result, code


def get_all_users():
    result, code = db.get_all(User)
    if result:
        if code == 200:  # if successful, returns the data
            users = [get_row_dict(u) for u in result]  # converts rows to dict
            return users, code
        return result, code  # else, returns database error and error code
    return [], 200


def get_one_user(username):
    result, code = db.get_one(User, username)

    if code == 200:  # if successful, returns the data
        user = get_row_dict(result)  # converts row to dict
        return user, 200
    return result, code  # else, returns database error and error code


def update_user(username, body):
    params = {}
    fields = ['email', 'username', 'full_name', 'password']

    for field in fields:
        if field in body:
            params[field] = body[field]

    errors = validate_update_user(body, params)
    if errors:
        return errors, 400

    result, code = db.update(User, username, params)

    if code == 200:  # if successful, returns the data
        user = get_row_dict(result)  # converts row to dict
        return user, code
    return result, code  # else, returns database error and error code


def delete_user(username):
    result, code = db.delete(User, username)

    return result, code
