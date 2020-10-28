import jwt

from settings import SECRET_KEY, BCRYPT
from database.db import get_one
from database.models import User
from utils.formatters import get_row_dict


def authentication(auth=None):
    if not auth:
        return "Login is required", 401

    if not auth['username'] or not auth['password']:
        return "Username and password are required", 401

    result, status = get_one(User, auth['username'])

    if status != 200:
        return result, status

    user = get_row_dict(result)

    if BCRYPT.check_password_hash(user['password'], auth['password']):
        token = jwt.encode(
            {
                'username': user['username'],
            },
            SECRET_KEY,
            algorithm='HS256'
        )
        return {
            'msg': 'Validated successfully',
            'token': token.decode('utf-8'),
        }, 200

    return 'Invalid password', 401
