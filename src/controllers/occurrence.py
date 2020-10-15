import datetime

from database.models import Occurrence
from database import db
from utils.validators.occurrence import (
    validate_create_occurrence,
    validate_update_occurrence,
    validate_occurrence_type
)
from settings import logger


def create_occurrence(username, body):

    errors = validate_create_occurrence(body)
    if errors:
        return errors, 400

    try:
        occurrence = Occurrence(
            user=username,
            occurrence_date_time=datetime.datetime.strptime(
                body['occurrence_date_time'], '%Y-%m-%d %H:%M:%S'),
            physical_aggression=body['physical_aggression'],
            victim=body['victim'],
            police_report=body['police_report'],
            gun=body['gun'],
            location=body['location'],
            occurrence_type=body['occurrence_type']
        )
        result, code = db.insert_one(occurrence)

        return result, code
    except Exception as error:
        logger.error(error)
        return str(error), 401


def get_all_occurrences(user=None, occurrences_types=None):
    # formating occurrences_types query param
    if (occurrences_types):
        occurrences_types = occurrences_types.split(',')
        # strip white spaces from start and end
        occurrences_types = list(map(lambda o: o.strip(), occurrences_types))
        # validating occurrences_types
        if (False in
                [validate_occurrence_type(occur_type)
                 for occur_type in occurrences_types]):
            return "occurrence_type inválido", 400

    result, code = db.get_all(Occurrence, user, occurrences_types)
    if result:
        if code == 200:  # if successful, returns the data
            # converts rows to dict
            occurrences = [occurrence.to_dict() for occurrence in result]
            return occurrences, code
        return result, code  # else, returns database error and error code
    return [], 200


def get_one_occurrence(id_occurrence):
    result, code = db.get_one(Occurrence, id_occurrence)

    if code == 200:  # if successful, returns the data
        occurrence = result.to_dict()  # converts row to dict
        return occurrence, 200
    return result, code  # else, returns database error and error code


def update_occurrence(id_occurrence, body):
    logger.info(id_occurrence)
    params = {}
    fields = ['occurrence_date_time', 'physical_aggression',
              'victim', 'police_report', 'gun', 'location', 'occurrence_type']

    for field in fields:
        if field in body:
            params[field] = body[field]

    errors = validate_update_occurrence(body, params)
    if errors:
        return errors, 400

    result, code = db.update(Occurrence, id_occurrence, params)

    if code == 200:  # if successful, returns the data
        occurrence = result.to_dict()  # converts row to dict
        return occurrence, code
    return result, code  # else, returns database error and error code


def delete_occurrence(id_occurrence):
    result, code = db.delete(Occurrence, id_occurrence)

    return result, code
