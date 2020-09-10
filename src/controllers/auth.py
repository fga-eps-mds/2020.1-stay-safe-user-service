import string
import random

def generateRandomString(tamanho):
    random_str = string.ascii_letters + string.digits + string.ascii_uppercase
    key = ''.join(random.choice(random_str)) for i in range(tamanho)
    return key

def auth(authorization):
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify ({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth=' 'Login required'}), 401

    return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

