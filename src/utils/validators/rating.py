from utils.validators.general import validate_fields, validate_fields_types


def validate_create_rating(body):
    fields = [
                ('rating_neighborhood', int), ('lighting', bool),
                ('movement_of_people', bool), ('police_rounds', bool)
             ]

    required_fields = [fields[0][0]]

    wrong_fields = validate_fields(body, required_fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Os seguintes campos estão faltando: {wrong_fields}'

    passed_fields = list(filter(lambda x: x[0] in body, fields))
    wrong_fields = validate_fields_types(body, passed_fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Campos com tipo inválido: {wrong_fields}'

    if 'rating_neighborhood' in body:
        if not validate_rating(body['rating_neighborhood']):
            return 'Nota inválida.'

    rating = body['rating_neighborhood']
    del body['rating_neighborhood']
    if body:
        if not validate_details(body, rating):
            return 'Detalhes da avaliação inválido.'

    return None


def validate_update_rating(params):
    fields = [
                ('rating_neighborhood', int), ('lighting', bool),
                ('movement_of_people', bool), ('police_rounds', bool)
             ]

    passed_fields = list(filter(lambda x: x[0] in body, fields))
    wrong_fields = validate_fields_types(params, passed_fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Campos com tipo inválido: {wrong_fields}'

    if 'rating_neighborhood' in params:
        if not validate_rating(params['rating_neighborhood']):
            return 'Nota inválida.'

    rating = body['rating_neighborhood']
    del body['rating_neighborhood']
    if body:
        if not validate_details(body, rating):
            return 'Detalhes da avaliação inválido.'

    return None


def validate_rating(rating):
    return True if rating in [1, 2, 3, 4, 5] else False


def validate_details(body, rating):
    for field, value in body.items():
        if (rating == 5 and value == False):
            return False
        if (rating == 1 and value == True):
            return False
    return True
