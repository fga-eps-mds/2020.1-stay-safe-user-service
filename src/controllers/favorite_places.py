from database.models import FavoritePlace
from database import db
from utils.formatters import get_row_dict
from utils.validators.favorite_places import validate_create_favorite_place
from settings import logger

def get_favorite_places(username):
    result, code = db.get_all(FavoritePlace, { 'user': [username] })

    if result:
        if code == 200:  # if successful, returns the data
            # converts rows to dict
            favorite_places = [get_row_dict(place) for place in result]
            return favorite_places, code
    return [], 200

def create_favorite_place(username, body):
    error = validate_create_favorite_place(body)
    if error:
        return error, 400
    
    try:
        place = FavoritePlace(
            user=username,
            name=body['name'],
            latitude=body['latitude'],
            longitude=body['longitude'],
        )
        result, code = db.insert_one(place)

        return result, code
    except Exception as error:
        logger.error(error)
        return str(error), 401

def delete_favorite_place(username, id_place):
    result, code = db.get_one(FavoritePlace, id_place)

    if code == 200:
        favorite_place = get_row_dict(result)

        if favorite_place['user'] != username:
            return "Unauthorized to delete this place." , 401

        result, code = db.delete(FavoritePlace, id_place)

    return result, code
