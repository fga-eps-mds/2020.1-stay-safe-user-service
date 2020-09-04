from database.models import User
from database import db
from utils.formatters import get_row_dict
from utils.validators import validate_create_user, validate_update_user
from settings import logger

def create_user(body):
    
    errors = validate_create_user(body)
    if (errors):
        return errors, 400
    
    user = User(username=body['username'], email=body['email'], password=body['password'], full_name=body['full_name'])
    result, code = db.insert_one(user)

    return result, code

def get_all_users():
    result, code = db.get_all(User)
    if result:
        if code == 200:  # if successful, returns the data
            users = [get_row_dict(u) for u in result]  # converts rows to dict
            return users, code
        return result, code  # else, returns database error and error code
    else:
        return [], 200


def get_one_user(username):
    result, code = db.get_one(User, username)
    if result:
        if code == 200:  # if successful, returns the data
            user = get_row_dict(result)  # converts row to dict
            return user, 200
        return result, code  # else, returns database error and error code
    else:
        return "User not found!", 404

def edit_user(username, body):
    params = {}
    if 'email' in body:
        params['email'] = body['email']
    if 'username' in body:
        params['username'] = body['username']
    if 'full_name' in body:
        params['full_name'] = body['full_name']
    if 'password' in body:
        params['password'] = body['password']

    errors = validate_update_user(body, params)
    if (errors):
        return errors, 400

    result, code = db.update(User, username, params)

    if result:
        if code == 200:  # if successful, returns the data
            user = get_row_dict(result)  # converts row to dict
            return user, 200
        return result, code  # else, returns database error and error code
    else:
        return "User not found!", 404

def delete_user(username):
    result, code = db.delete(User, username)

    return result, code
