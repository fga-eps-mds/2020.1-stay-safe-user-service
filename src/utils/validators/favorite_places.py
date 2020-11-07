from utils.validators.general import validate_fields

def validate_create_favorite_place(body):
    fields = [('name', str), ('longitude', float), ('latitude', float)]

    required_fields = [f[0] for f in fields]

    wrong_fields = validate_fields(body, required_fields)
    if wrong_fields:
        wrong_fields = ", ".join(wrong_fields)
        return f'Os seguintes campos estão faltando: {wrong_fields}'

    if len(body['name']) < 1 or len(body['name']) > 30:
        return 'Campo name com tamanho inválido!'

    return None