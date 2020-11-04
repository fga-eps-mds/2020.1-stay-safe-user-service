import datetime

from database.models import Occurrence
from database import db
from utils.validators.occurrence import (
    validate_create_occurrence,
    validate_update_occurrence,
    validate_occurrence_type
)
from settings import logger
from utils.utils import get_params_by_body


def create_occurrence(username, body):

    last_occurrences, code = db.get_all(Occurrence,
                                        filter={'user': [username]})
    if code != 200:
        return "Erro ao carregar ocorrências antigas"

    errors = validate_create_occurrence(body, last_occurrences)
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


def get_all_occurrences(user=None, occurrence_type=None):
    filter_ = {} if user or occurrence_type else None
    # formating occurrence_type query param
    if occurrence_type:
        occurrence_type = occurrence_type.split(',')

        # strip white spaces from start and end
        occurrence_type = [o.strip() for o in occurrence_type]

        # validating occurrence_type
        if (False in
                [validate_occurrence_type(occur_type)
                 for occur_type in occurrence_type]):
            return "occurrence_type inválido", 400

        filter_.update({"occurrence_type": occurrence_type})

    if user:
        filter_.update({'user': [user]})

    result, code = db.get_all(Occurrence, filter_)
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


def update_occurrence(id_occurrence, body, username=None):
    current_occurrence, code = db.get_one(Occurrence, id_occurrence)
    if (code != 200):
        return "Erro ao achar ocorrência", code

    fields = ['occurrence_date_time', 'physical_aggression',
              'victim', 'police_report', 'gun', 'location', 'occurrence_type']

    params = get_params_by_body(fields, body)

    errors = validate_update_occurrence(body, params, current_occurrence)
    if errors:
        return errors, 400

    result, code = db.update(Occurrence, id_occurrence, params, username)

    if code == 200:  # if successful, returns the data
        occurrence = result.to_dict()  # converts row to dict
        return occurrence, code
    return result, code  # else, returns database error and error code


def delete_occurrence(id_occurrence, username=None):
    result, code = db.delete(Occurrence, id_occurrence, username)

    return result, code
