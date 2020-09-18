import jwt
from werkzeug.security import safe_str_cmp

from settings import SECRET_KEY
from .user import get_one_user


def authentication(auth):
    if not auth or not auth['username'] or not auth['password']:
        return 'Login required', 401

    result, status = get_one_user(auth['username'])

    if status != 200:
        return result, status

    user = result

    user_password = user['password'].encode('utf-8')
    auth_password = auth['password'].encode('utf-8')
    if safe_str_cmp(auth_password, user_password):
        token = jwt.encode(
            {
                'username': user['username'],
            },
            SECRET_KEY,
            algorithm='HS256'
        )
        return {
            'msg': 'Validated successfully',
            'token': token.decode('UTF-8'),
        }, 200

    return 'Invalid password', 401
