from utils.validators.general import validate_fields, validate_fields_types
import datetime


def validate_create_occurrence(body):
    fields = [
        ('physical_aggression', bool), ('victim', bool),
        ('police_report', bool), ('gun', str),
        ('location', list), ('occurrence_type', str),
        ('occurrence_date_time', str)
    ]

    required_fields = [f[0] for f in fields]
    error = None

    wrong_fields = validate_fields(body, required_fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        error = f'Os seguintes campos estão faltando: {wrong_fields}'

    wrong_fields = validate_fields_types(body, fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        error = f'Campos com tipo inválido: {wrong_fields}'

    if not validate_occurrence_date_time(body['occurrence_date_time']):
        error = "Data de Ocorrência inválida."

    if not validate_gun(body['gun']):
        error = "Arma inválida."

    if not validate_occurrence_type(body['occurrence_type']):
        error = "Tipo de Ocorrência inválida."

    return error


def validate_update_occurrence(body, params, current_occurrence):
    # check if occurrence is 3 months old
    allowed_date = datetime.datetime.utcnow()\
                        .replace(month=datetime.datetime.utcnow().month - 3)\
                        .date()
    if current_occurrence.register_date_time.date() < allowed_date:
        return "A ocorrência não pode ser mais editada."

    available_fields_types = {
        'physical_aggression': bool, 'victim': bool, 'police_report': bool,
        'gun': str, 'location': list, 'occurrence_type': str
    }
    fields = []
    error = None
    for param in params:
        if param != 'occurrence_date_time':
            fields.append((param, available_fields_types[param]))

    wrong_fields = validate_fields_types(body, fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        error = f'Campos com tipo inválido: {wrong_fields}'

    if 'occurrence_date_time' in body:
        if not validate_occurrence_date_time(body['occurrence_date_time']):
            error = "Data de Ocorrẽncia inválida."

    if 'gun' in body:
        if not validate_gun(body['gun']):
            error = "Arma inválida."

    if 'occurrence_type' in body:
        if not validate_occurrence_type(body['occurrence_type']):
            error = "Tipo de Ocorrência inválida."

    return error


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


def validate_fields_length(json):
    errors = []

    if 'username' in json:
        if len(json['username']) < 3 or len(json['username']) > 20:
            errors.append('username')

    if 'email' in json:
        if len(json['email']) < 6 or len(json['email']) > 50:
            errors.append('email')

    if 'password' in json:
        if len(json['password']) < 6 or len(json['password']) > 20:
            errors.append('password')

    if 'full_name' in json:
        if len(json['full_name']) < 1 or len(json['full_name']) > 200:
            errors.append('full_name')

    return errors
