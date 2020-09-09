from database.models import Occurrence
from database import db
from utils.formatters import get_row_dict
import datetime
# from utils.validators import validate_create_user, validate_update_user


def create_occurrence(body):

    # THE VALIDATION IT WILL BE CREATED AFTER THE ROUTES
    # errors = validate_create_user(body)
    # if errors:
    #     return errors, 400

    occurrence = Occurrence(
        # REQUIRES THE AUTHENTICATION ISSUE
        # FOR NOW IT WILL BE USED A USER THAT ALREADY EXISTS ON THE DB
        user = body['user'],
        occurrence_date_time = datetime.datetime.strptime(body['occurrence_date_time'], '%d/%m/%y %H:%M:%S'),
        physical_aggression = body['physical_aggression'],
        victim = body['victim'],
        police_report = body['police_report'],
        gun = body['gun'],
        location = body['location'],
        occurence_type = body['occurence_type']
    )
    result, code = db.insert_one(occurrence)

    return result, code


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
    fields = ['email', 'id', 'full_name', 'password']

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
