import jwt
import string
import random
import datetime
from settings import logger
from flask import request
from .user import get_one_user
from views import user
from utils.formatters import create_response
from werkzeug.security import check_password_hash

def generate_random_key(size):
    random_str = string.ascii_letters + string.digits + string.ascii_uppercase
    key = ''.join(random.choice(random_str) for i in range(size))
    return key

def authentication(auth):
    if not auth or not auth.username or not auth.password:
        return 'Login required', 401

    result, status = get_one_user(auth.username)
    
    if status != 200:
        return result,status

    user =  result

    if auth.password == user['password']:        
        token = jwt.encode(
            {
                'username': user['username'] 
            },
            generate_random_key(10)
        )
        return  {
                    'msg': 'Validated successfully', 'token': token.decode('UTF-8')
                }, 200

    return 'Invalid password', 401

