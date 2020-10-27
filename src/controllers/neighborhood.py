from database.models import Neighborhood, Rating
from database import db
from utils.formatters import get_row_dict
from utils.neighborhood_statistics import get_neighborhood_statistics
from settings import logger


def create_neighborhood(body):

    try:
        neighborhood = Neighborhood(
            neighborhood=body['neighborhood'],
            city=body['city'],
            state=body['state']
        )
        result, code = db.insert_one(neighborhood)

        return result, code
    except Exception as error:
        logger.error(error)
        return str(error), 401


def get_all_neighborhoods():
    result, code = db.get_all(Neighborhood)
    if result:
        if code == 200:
            neighborhoods = [get_row_dict(u) for u in result]
            return neighborhoods, code
        return result, code
    return [], 200


def get_one_neighborhood(neighborhood_id):
    result, code = db.get_one(Neighborhood, neighborhood_id)

    # formating filter
    filter_ = {"id_neighborhood": [neighborhood_id]}
    ratings, status = db.get_all(Rating, filter_)
    ratings = [get_row_dict(rat) for rat in ratings]

    if code == 200:
        neighborhood = get_row_dict(result)
        if ratings:
            statistics = get_neighborhood_statistics(ratings)
            neighborhood.update(statistics)
        return neighborhood, 200
    return result, code


def delete_neighborhood(neighborhood_id):
    result, code = db.delete(Neighborhood, neighborhood_id)

    return result, code
