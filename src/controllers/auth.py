import jwt

from settings import SECRET_KEY, BCRYPT
from controllers.user import get_one_user


def authentication(auth=None):
    status = 401
    response = 'Invalid password'
    if not auth:
        response = "Login is required"
    elif not auth['username'] or not auth['password']:
        response = "Username and password are required"
    else:
        result, status_ = get_one_user(auth['username'])
        if status_ == 200:
            user = result
            if BCRYPT.check_password_hash(user['password'], auth['password']):
                token = jwt.encode(
                    {
                        'username': user['username'],
                    },
                    SECRET_KEY,
                    algorithm='HS256'
                )
                status = 200
                response = {
                    'msg': 'Validated successfully',
                    'token': token.decode('utf-8'),
                }
        else:
            response = result
            status = status_
    return response, status
