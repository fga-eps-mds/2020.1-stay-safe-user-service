from utils.validators.general import validate_fields, validate_fields_types
import datetime


def validate_create_occurrence(body, last_ocurrences):
    if len(last_ocurrences) >= 5:
        last_ocurrence = last_ocurrences[4]
        if (datetime.datetime.utcnow().date() -
                last_ocurrence.register_date_time.date()).days < 7:
            return "The limit of 5 occurrences within 7 days was reached."

    fields = [
        ('physical_aggression', bool), ('victim', bool),
        ('police_report', bool), ('gun', str),
        ('location', list), ('occurrence_type', str),
        ('occurrence_date_time', str)
    ]

    required_fields = [f[0] for f in fields]

    wrong_fields = validate_fields(body, required_fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'The following fields are missing: {wrong_fields}'

    wrong_fields = validate_fields_types(body, fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Fields with invalid type: {wrong_fields}'

    if not validate_occurrence_date_time(body['occurrence_date_time']):
        return "Invalid occurrence date."

    if not validate_gun(body['gun']):
        return "Invalid gun."

    if not validate_occurrence_type(body['occurrence_type']):
        return "Invalid occurrence type."

    return None


def validate_update_occurrence(body, params, current_occurrence):
    # check if occurrence is 3 months old
    allowed_date = datetime.datetime.utcnow()\
                        .replace(month=datetime.datetime.utcnow().month - 3)\
                        .date()
    if current_occurrence.register_date_time.date() < allowed_date:
        return "The occurrence cannot be edited."

    available_fields_types = {
        'physical_aggression': bool, 'victim': bool, 'police_report': bool,
        'gun': str, 'location': list, 'occurrence_type': str
    }
    fields = []
    
    for param in params:
        if param != 'occurrence_date_time':
            fields.append((param, available_fields_types[param]))

    wrong_fields = validate_fields_types(body, fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Fields with invalid type: {wrong_fields}'

    if 'occurrence_date_time' in body:
        if not validate_occurrence_date_time(body['occurrence_date_time']):
            return "Invalid occurrence date."

    if 'gun' in body:
        if not validate_gun(body['gun']):
            return "Invalid gun."

    if 'occurrence_type' in body:
        if not validate_occurrence_type(body['occurrence_type']):
            return "Invalid occurrence type."

    return None


def validate_occurrence_date_time(occurrence_date_time):
    delta_time = datetime.datetime.now() - datetime.datetime.strptime(
        occurrence_date_time, '%Y-%m-%d %H:%M:%S')
    if delta_time.days > 365 or delta_time.days < 0:
        return False
    return True


def validate_gun(gun):
    available_guns = ["None", 'White', 'Fire']
    if (gun not in available_guns):
        return False
    return True


def validate_occurrence_type(occurrence_type):
    available_occurrence_type = ['Latrocínio', 'Roubo a Transeunte',
                                 'Roubo de Veículo', 'Roubo de Residência',
                                 'Estupro', 'Furto a Transeunte',
                                 'Furto de Veículo']
    if (occurrence_type not in available_occurrence_type):
        return False
    return True
