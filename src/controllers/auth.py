import string
import random

def generateRandomString(tamanho):
    random_str = string.ascii_letters + string.digits + string.ascii_uppercase
    key = ''.join(random.choice(random_str)) for i in range(tamanho)
    return key

