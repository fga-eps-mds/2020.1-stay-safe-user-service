
def validate_fields(json, *fields):
    '''Valida se o json possui os campos informados
    Para verificar se há um dicionário dentro de outro, separe as chaves por /
    Ex: validate_fields({'msg': {'content':'Hello World'}}, 'msg/content')

    Parâmetros:
        - json a ser validado -> dict
        - campos a serem verificados -> *str

    Retorno:
        - Lista com os campos não encontrados ou lista vazia
    '''

    try:
        errors = []
        for field in fields:
            f = field.split('/')
            f = list(filter(None, f))
            if len(f) == 1:
                if f[0] not in json:
                    errors.append(f[0])
            else:
                if f[0] in json:
                    err = validate_fields(json[f[0]], '/'.join(f[1:]))
                    if err:
                        errors.append(err[0])
                else:
                    errors.append(f[0])
        return errors
    except Exception:
        return ['json inválido']


def validate_fields_types(json, params):
    '''Valida os tipos dos campos em um json

    Parâmetros:
        - json
        - params -> lista de tupla composta por campo e valor

    Retorno:
        - lista com erros encontrados ou lista vazia
    '''
    errors = []
    for field, value_type in params:
        if not isinstance(json[field], value_type):
            errors.append(field)
    return errors