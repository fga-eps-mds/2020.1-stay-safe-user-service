from database.models import Rating, Neighborhood
from database import db
from utils.formatters import get_row_dict
from utils.validators.rating import (
    validate_create_rating,
    validate_update_rating
)
from settings import logger


def create_rating(body, username, neighborhood_id):

    neighborhood, code = db.get_one(Neighborhood, neighborhood_id)

    if code == 404:
        return 'Bairro não existe', 404

    errors = validate_create_rating(body)
    if errors:
        return errors, 400
    # return "aa", 200

    details = {}
    for attr in body:
        if attr != "rating_neighborhood" :
            details[attr] = body[attr]

    try:
        rating = Rating(
            user=username,
            id_neighborhood=neighborhood_id,
            rating_neighborhood=body['rating_neighborhood'],
            details=details
        )
        result, code = db.insert_one(rating)

        return result, code
    except Exception as error:
        logger.error(error)
        return str(error), 401


def get_all_ratings(user=None, neighborhood=None):
    # formatting filters
    filter = {} if user or neighborhood else None
    if (user):
        filter.update({'user': [user]})
    if (neighborhood):
        filter.update({'neighborhood': [neighborhood]})

    result, code = db.get_all(Rating, filter)
    for i in range(len(result)):
        result[i].details = result[i].details._asdict()
        # for attr, value in result[i].details.items():
        #     if value == None:
        #         del result.details[attr]
    if result:
        if code == 200:
            ratings_neighborhood = [get_row_dict(u) for u in result]
            return ratings_neighborhood, code
        return result, code
    return [], 200


def get_one_rating(rating_id):
    result, code = db.get_one(Rating, rating_id)        

    if code == 200:
        result.details = result.details._asdict()
        for attr, value in result.details.items():
            if value == None:
                del result.details[attr]
        rating = get_row_dict(result)
        return rating, 200
    return result, code


def delete_rating(rating_id, username=None):
    result, code = db.delete(Rating, rating_id, username)

    return result, code


def update_rating(rating_id, body, username=None):
    params = {}
    fields = ['rating_neighborhood']

    result, status = db.get_one(Rating, rating_id)
    rating_before_update = get_row_dict(result)

    if status == 404:
        return 'Avaliação não existe', 404

    for field in fields:
        if field in body:
            params[field] = body[field]
        else:
            params[field] = rating_before_update[field]

    errors = validate_update_rating(params)
    if errors:
        return errors, 400

    result, code = db.update(Rating, rating_id, params, username)

    if code == 200:
        rating = get_row_dict(result)
        return rating, code

    return result, code
