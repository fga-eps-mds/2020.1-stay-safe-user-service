from database.models import Neighborhood
from database import db
from utils.formatters import get_row_dict
from settings import logger
from controllers import rating as rating_controller


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
    # ratings, status = rating_controller.get_all_ratings(neighborhood=neighborhood_id)
    if code == 200:
        neighborhood = get_row_dict(result)
        return neighborhood, 200
    return result, code


def delete_neighborhood(neighborhood_id):
    result, code = db.delete(Neighborhood, neighborhood_id)

    return result, code
