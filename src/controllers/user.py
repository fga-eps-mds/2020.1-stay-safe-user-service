from database.models import User
from database import db
from utils.formatters import get_row_dict


def create_user(body):
    user = User(cpf=body['cpf'], name=body['name'], email=body['email'])
    result, code = db.insert_one(user)

    return result, code


def get_all_users():
    result, code = db.get_all(User)

    if result:
        if code >= 200:  # if successful, returns the data
            users = [get_row_dict(u) for u in result]  # converts rows to dict
            return users, code
        return result, code  # else, returns database error and error code
    else:
        return [], 200


def get_one_user(cpf):
    result, code = db.get_one(User, cpf)
    if result:
        if code >= 200:  # if successful, returns the data
            user = get_row_dict(result)  # converts row to dict
            return user, 200
        return result, code  # else, returns database error and error code
    else:
        return "User not found!", 404


def delete_user(cpf):
    result, code = db.delete(User, cpf)

    return result, code
