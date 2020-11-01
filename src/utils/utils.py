def get_params_by_body(fields, body):
    params = {}
    for field in fields:
        if field in body:
            params[field] = body[field]
    return params
