from validate_email import validate_email


def validate_create_user(body):
  fields = validate_fields(body, 'username', 'email', 'full_name', 'password')
  if(fields):
    error = "Campo(s) "
    error += str(fields)
    error += " não encontrados"
    return error

  fields = validate_fields_types(body, [('username', str), ('email', str), ('full_name', str), ('password', str)])
  if(fields):
    error = "Campo(s) "
    error += str(fields)
    error += " não batem com seu respectivo tipo."
    return error
  
  fields = validate_fields_length(body)
  if (fields):
    error = "Campo(s) "
    error += str(fields)
    error += " com tamanhos errados."
    return error

  if(not validate_email(body['email'])):
    return "Email inválido"

  username_is_valid = validate_username(body['username'])
  if (username_is_valid):
    return username_is_valid

  if (body['password'].isalpha()):
    return "A senha deve conter pelo menos um número."
    
  return False

def validate_update_user(body, params):
  fields = []
  for param in params:
    fields.append((param, str))
  is_valid = validate_fields_types(body, fields)
  if(is_valid):
    error = "Campo(s) "
    error += str(fields)
    error += " não batem com seu respectivo tipo."
    return error

  fields = validate_fields_length(body)
  if (fields):
    error = "Campo(s) "
    error += str(fields)
    error += " com tamanhos errados."
    return error

  if(not validate_fields(body, 'email')):
    if(not validate_email(body['email'])):
      return "Email inválido"

  if(not validate_fields(body, 'username')):
    username_is_valid = validate_username(body['username'])
    if (username_is_valid):
      return username_is_valid

  if (not validate_fields(body, 'password')):
    if (body['password'].isalpha()):
      return "A senha deve conter pelo menos um número."
    
  return False

def validate_username(username):
  errors = []
  if (username.count(' ') > 0):
    errors.append("O username não pode conter espaços.")

  if (not username.isalnum()):
    errors.append("O username pode conter apenas letras e números.")

  if (errors):
    return errors
  return False

def validate_fields_length(json):
  errors = []
  if (not validate_fields(json, 'username')):
    if (len(json['username']) < 3 or len(json['username']) > 20):
      errors.append('username')

  if (not validate_fields(json, 'email')):
    if (len(json['email']) < 6 or len(json['email']) > 50):
      errors.append('email')
    
  if (not validate_fields(json, 'password')):
    if (len(json['password']) < 6 or len(json['password']) > 20):
      errors.append('password')

  if (not validate_fields(json, 'full_name')):
    if (len(json['full_name']) < 1 or len(json['full_name']) > 200):
      errors.append('full_name')

  if (errors):
    return errors
  return False

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
