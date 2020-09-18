from utils.validators.general import validate_fields, validate_fields_types


def validate_create_rating(body):
    fields = [('rating_neighborhood', int), ('details', str)]

    required_fields = [f[0] for f in fields]

    wrong_fields = validate_fields(body, required_fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Os seguintes campos estão faltando: {wrong_fields}'

    wrong_fields = validate_fields_types(body, fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Campos com tipo inválido: {wrong_fields}'

    if 'rating_neighborhood' in body:
        if not validate_rating(body['rating_neighborhood']):
            return 'Nota inválida.'

    if 'details' in body:
        if not validate_details(body['details'], body['rating_neighborhood']):
            return 'Detalhe da avaliação inválido.'

    return None


def validate_update_rating(body, params):
    fields = [
        ('rating_neighborhood', int),
        ('details', str)
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

    if 'rating_neighborhood' in body:
        if not validate_rating(body['rating_neighborhood']):
            return 'Nota inválida.'

    if 'details' in body:
        if not validate_details(body['details'], body['rating_neighborhood']):
            return 'Detalhe da avaliação inválido.'

    return None


def validate_rating(rating):
    return True if rating in [1, 2, 3, 4, 5] else False


def validate_details(details, rating):
    available_details = ["bad lighting", "low movement of people",
                        "few police rounds", "good lighting",
                        "good movement of people", "frequent police rounds"]

    if details not in available_details:
        return False

    if rating <= 2 and details not in available_details[0:3]:
        return False

    if rating >= 4 and details not in available_details[3:6]:
        return False

    return True
