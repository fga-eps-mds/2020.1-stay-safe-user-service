from utils.validators.general import validate_fields, validate_fields_types
import datetime


def validate_create_occurrence(body, last_ocurrences):
    if len(last_ocurrences) >= 5:
        last_ocurrence = last_ocurrences[4]
        if (datetime.datetime.utcnow().date() -
                last_ocurrence.register_date_time.date()).days < 7:
            return "O limite de 5 ocorrências em 7 dias foi atingido"

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
        return f'Os seguintes campos estão faltando: {wrong_fields}'

    wrong_fields = validate_fields_types(body, fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Campos com tipo inválido: {wrong_fields}'

    if not validate_occurrence_date_time(body['occurrence_date_time']):
        return "Data da ocorrência inválida"

    if not validate_gun(body['gun']):
        return "Tipo de arma inválido"

    if not validate_occurrence_type(body['occurrence_type']):
        return "Tipo de ocorrência inválido"

    return None


def validate_update_occurrence(body, params, current_occurrence):
    # check if occurrence is 3 months old
    allowed_date = datetime.datetime.utcnow()\
                        .replace(month=datetime.datetime.utcnow().month - 3)\
                        .date()
    if current_occurrence.register_date_time.date() < allowed_date:
        return "A ocorrência não pode ser editada"

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
        return f'Campos com tipo inválido: {wrong_fields}'

    if 'occurrence_date_time' in body:
        if not validate_occurrence_date_time(body['occurrence_date_time']):
            return "Data da ocorrência inválida"

    if 'gun' in body:
        if not validate_gun(body['gun']):
            return "Tipo de arma inválido"

    if 'occurrence_type' in body:
        if not validate_occurrence_type(body['occurrence_type']):
            return "Tipo de ocorrência inválido"

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
    available_occurrence_type = ['Latrocínio', 'Roubo a Pedestre',
                                 'Roubo de Veículo', 'Roubo de Residência',
                                 'Estupro', 'Furto a Pedestre',
                                 'Furto de Veículo']
    if (occurrence_type not in available_occurrence_type):
        return False
    return True
