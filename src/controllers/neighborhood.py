from database.models import Neighborhood
from database import db
from utils.formatters import get_row_dict
from settings import logger


def create_neighborhood(body, header):

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


def delete_neighborhood(id):
    result, code = db.delete(Neighborhood, id)

    return result, code
