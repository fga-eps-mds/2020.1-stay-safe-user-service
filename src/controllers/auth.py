import jwt

from settings import SECRET_KEY, BCRYPT
from controllers.user import get_one_user


def authentication(auth):
    if not auth['username'] or not auth['password']:
        return "Username and password are required", 401

    result, status = get_one_user(auth['username'])

    if status != 200:
        return result, status

    user = result

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
