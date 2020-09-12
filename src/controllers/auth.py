import jwt
import string
import random
import datetime
from werkzeug.security import safe_str_cmp

from settings import logger, SECRET_KEY
from flask import request
from .user import get_one_user
from views import user
from utils.formatters import create_response


def authentication(auth):
    if not auth or not auth.username or not auth.password:
        return 'Login required', 401

    result, status = get_one_user(auth.username)
    
    if status != 200:
        return result,status

    user =  result

    if safe_str_cmp(auth.password.encode('utf-8'), user['password'].encode('utf-8')):
        token = jwt.encode(
            {
                'username': user['username'],
            },
            SECRET_KEY
        )
        return  {
                    'msg': 'Validated successfully',
                    'token': token.decode('UTF-8'),
                }, 200

    return 'Invalid password', 401

