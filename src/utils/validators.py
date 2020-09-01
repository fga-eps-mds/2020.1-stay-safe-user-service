def validate_user(body):
  if(validate_fields(body, 'username', 'email', 'full_name', 'password')):
    return "Campos não encontrados"
  
  if(validate_fields_types(body, [('username', str), ('email', str), ('full_name', str), ('password', str)])):
    return "Campos não batem com seu respectivo tipo(string)."
  
  if (not validate_fields_length(body)):
    return "Campos com tamanhos errados"

  return False

def validate_fields_length(json):
  if (len(json['username']) < 3 or len(json['username']) > 20):
    return False

  if (len(json['email']) < 6 or len(json['email']) > 50):
    return False
    
  if (len(json['password']) < 6 or len(json['password']) > 20):
    return False

  if (len(json['full_name']) < 1 or len(json['full_name']) > 200):
    return False

  return True

def validate_fields(json, *fields):
    '''Validates if the json has the right attributes
    To verify a dict inside a dict, separate the keys with /
    Ex: validate_fields({'msg': {'content':'Hello World'}}, 'msg/content')

    Parameters:
        - JSON to be validated-> dict
        - fields to be verified -> *str

    Return:
        - Lists attributes not found or empty list
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
        return ['Invalid JSON']


def validate_fields_types(json, params):
    '''Validates the fields types in a JSON

    Parameters:
        - JSON
        - params -> tuple list composed by a field and a value

    Return:
        - Lists attributes not found or empty list
    '''
    errors = []
    for field, value_type in params:
        if not isinstance(json[field], value_type):
            errors.append(field)
    return errors