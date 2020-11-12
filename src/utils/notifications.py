import json
import requests
from settings import logger


def send_notification_on_signin(user, username):
    token = user['device_token'] if user['device_token'] != '' and user['device_token'] != None else body['device_token']

    message = {
        'to': token,
        'sound': 'default',
        'title': 'Bem-vind@',
        'body': f'Estamos felizes em te receber, {username}, aproveite e fique sempre seguro!',
        'data': {'data': 'goes here'},
    }

    headers = {
        "Accept": "*/*",
        'Accept-encoding': 'gzip, deflate',
        "Content-Type": "application/json"
    }

    a = requests.post('https://exp.host/--/api/v2/push/send',
                      data=json.dumps(message), headers=headers)

    logger.info(message)
