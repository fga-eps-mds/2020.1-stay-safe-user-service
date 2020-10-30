from database.models import Rating, Neighborhood
from database import db
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

    details = dict(filter(
                          lambda x: x[0] != 'rating_neighborhood',
                          body.items()
                         )
                   )

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
    if user:
        filter.update({'user': [user]})
    if neighborhood:
        filter.update({'id_neighborhood': [neighborhood]})

    result, code = db.get_all(Rating, filter)

    if result:
        if code == 200:
            ratings_neighborhood = [u.to_dict() for u in result]
            return ratings_neighborhood, code
        return result, code
    return [], 200


def get_one_rating(rating_id):
    result, code = db.get_one(Rating, rating_id)

    if code == 200:
        rating = result.to_dict()
        return rating, 200
    return result, code


def delete_rating(rating_id, username=None):
    result, code = db.delete(Rating, rating_id, username)

    return result, code


def update_rating(rating_id, body, username=None):

    result, status = db.get_one(Rating, rating_id)
    rating_before_update = result.to_dict(del_null_attr=False)

    if status == 404:
        return 'Avaliação não existe', 404

    errors = validate_update_rating(body, rating_before_update)
    if errors:
        return errors, 400

    details = []
    for attr, value in rating_before_update['details'].items():
        if attr in body:
            details.append(body[attr])
        else:
            details.append(value)
    body = dict(filter(lambda x: x[0] == 'rating_neighborhood', body.items()))
    body['details'] = details

    result, code = db.update(Rating, rating_id, body, username)

    if code == 200:
        rating = result.to_dict()
        return rating, code

    return result, code
