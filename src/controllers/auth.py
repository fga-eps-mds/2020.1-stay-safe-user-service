import jwt

from settings import SECRET_KEY, BCRYPT
from database.db import get_one
from database.models import User
from utils.formatters import get_row_dict


def authentication(auth=None):
    if not auth:
        status = 401
        response = "É necessário realizar o login"
    elif not auth['username'] or not auth['password']:
        status = 401
        response = "O nome de usuário e senha são obrigatórios"
    else:
        result, status_ = get_one(User, auth['username'])
        if status_ == 200:
            response, status = get_auth_response(result, auth)
        else:
            response = result
            status = status_
    return response, status


def get_auth_response(user, auth):
    user = get_row_dict(user)
    if BCRYPT.check_password_hash(user['password'], auth['password']):
        token = jwt.encode(
            {
                'username': user['username'],
            },
            SECRET_KEY,
            algorithm='HS256'
        )
        return {
            'msg': 'Login bem sucedido',
            'token': token.decode('utf-8'),
        }, 200
    return 'Senha inválida', 401
