from database.models import Rating, Neighborhood
from database import db
from utils.formatters import get_row_dict
import jwt
from utils.validators.rating import (
    validate_create_rating,
    validate_update_rating
)
from settings import logger, SECRET_KEY

def create_rating(body, header, id):
    
    neighborhood = db.get_one(Neighborhood, id)

    if neighborhood[1] == 404:
        return 'Bairro não existe', 404

    errors = validate_create_rating(body)
    if errors:
        return errors, 400

    try:
        username = jwt.decode(header['Authorization'], SECRET_KEY, algorithms=[
                              'HS256'])['username']
        rating = Rating(
            user=username,
            id_neighborhood=id,
            rating_neighborhood=body['rating_neighborhood'],
            details=body['details'],
        )
        result, code = db.insert_one(rating)

        return result, code
    except Exception as error:
        logger.error(error)
        return str(error), 401


def get_all_ratings():
    result, code = db.get_all(Rating)
    if result:
        if code == 200:  # if successful, returns the data
            ratings_neighborhood = [get_row_dict(u)
                           for u in result]  # converts rows to dict
            return ratings_neighborhood, code
        return result, code  # else, returns database error and error code
    return [], 200


def get_one_rating(id):
    result, code = db.get_one(Rating, id)

    if code == 200: 
        rating = get_row_dict(result)
        return rating, 200
    return result, code


def delete_rating(id):
    result, code = db.delete(Rating, id)

    return result, code


def update_rating(id, body):
    params = {}
    fields = ['rating_neighborhood', 'details']

    for field in fields:
        if field in body:
            params[field] = body[field]
    
    errors = validate_update_rating(body, params)
    if errors:
        return errors, 400

    result, code = db.update(Rating, id, params)

    if code == 200:  # if successful, returns the data
        rating = get_row_dict(result)  # converts row to dict
        return rating, code

    return result, code
