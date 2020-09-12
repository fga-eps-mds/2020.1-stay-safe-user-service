from database.models import Occurrence
from database import db
from utils.formatters import get_row_dict
import datetime
import jwt
from utils.validators.occurrence import validate_create_occurrence, validate_update_occurrence
from settings import logger, SECRET_KEY

def create_occurrence(body, header):

    errors = validate_create_occurrence(body)
    if errors:
        return errors, 400

    try:
        username = jwt.decode(header['Authorization'], SECRET_KEY, algorithms=['HS256'])['username']
        occurrence = Occurrence(
            user = username,
            occurrence_date_time = datetime.datetime.strptime(body['occurrence_date_time'], '%Y-%m-%d %H:%M:%S'),
            physical_aggression = body['physical_aggression'],
            victim = body['victim'],
            police_report = body['police_report'],
            gun = body['gun'],
            location = body['location'],
            occurrence_type = body['occurrence_type']
        )
        result, code = db.insert_one(occurrence)

        return result, code
    except Exception as error:
        logger.error(error)
        return str(error), 401



def get_all_occurrences():
    result, code = db.get_all(Occurrence)
    if result:
        if code == 200:  # if successful, returns the data
            occurrences = [get_row_dict(u) for u in result]  # converts rows to dict
            return occurrences, code
        return result, code  # else, returns database error and error code
    return [], 200


def get_one_occurrence(id):
    result, code = db.get_one(Occurrence, id)

    if code == 200:  # if successful, returns the data
        occurrence = get_row_dict(result)  # converts row to dict
        return occurrence, 200
    return result, code  # else, returns database error and error code


def update_occurrence(id, body):
    params = {}
    fields = ['occurrence_date_time', 'physical_aggression', 'victim', 'police_report', 'gun', 'location', 'occurrence_type']

    for field in fields:
        if field in body:
            params[field] = body[field]

    errors = validate_update_occurrence(body, params)
    if errors:
        return errors, 400

    result, code = db.update(Occurrence, id, params)

    if code == 200:  # if successful, returns the data
        occurrence = get_row_dict(result)  # converts row to dict
        return occurrence, code
    return result, code  # else, returns database error and error code


def delete_occurrence(id):
    result, code = db.delete(Occurrence, id)

    return result, code
