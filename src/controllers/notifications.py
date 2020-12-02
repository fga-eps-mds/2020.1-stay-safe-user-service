import requests
import json

from database.db import get_all, get_one
from database.models import FavoritePlace, User
from utils.formatters import get_row_dict
from utils.utils import haversine


def send_notifications_near_occcurrences(occurrence, username):
    result, code = get_all(FavoritePlace)

    favorite_places = [get_row_dict(u) for u in result]

    near_favorite_places = set()

    for favorite_place in favorite_places:
        if haversine(favorite_place, occurrence) != None:
            user = get_row_dict(get_one(User, favorite_place['user'])[0])

            if user['show_notifications'] and user['username'] != username:
                near_favorite_places.add(
                    user['device_token'])

    message = {
        'to': [token for token in near_favorite_places],
        'sound': 'default',
        'title': 'Atenção!',
        'body': f'Uma ocorrência foi reportada perto de um de seus locais favoritos!',
        'data': {'data': occurrence},
    }

    headers = {
        "Accept": "*/*",
        'Accept-encoding': 'gzip, deflate',
        "Content-Type": "application/json"
    }

    response = requests.post('https://exp.host/--/api/v2/push/send',
                             data=json.dumps(message), headers=headers)

    return occurrence, 200
