import string
import random
from  utils.formatters import create_response

def generateRandomString(tamanho):
    random_str = string.ascii_letters + string.digits + string.ascii_uppercase
    key = ''.join(random.choice(random_str)) for i in range(tamanho)
    return key

def auth(authorization):
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return create_response({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth=' 'Login required'}, 401)

    user, _ = get_one_user(auth.username)

    if not user:
        return create_response({'message': 'user not found', 'data': {}}, 401)
    
    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode({'username': user.name, 'exp': datetime.datetime.now() + datetime.timedelta(hours=12) },
        app.config['key'])
        return create_response({'message': 'Validated successfully', 'token': token.decode('UTF-8'),
                'exp': datetime.datetime.now() + datetime.timedelta(hours = 12)})

    return create_response({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}, 401)

