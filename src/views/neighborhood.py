from functools import wraps
from flask import Blueprint, request
from flask_cors import CORS

from controllers import neighborhood as controller
from utils.formatters import create_response

neighborhood_blueprint = Blueprint('neighborhood', __name__, url_prefix='/api')
CORS(neighborhood_blueprint)


def validate_header(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        type_error = ('Unsupported media type', 415)
        header_values = ['*/*', 'application/json']
        header_keys = ['Accept', 'Content-Type']
        header = request.headers
        rm = request.method
        methods = ['POST', 'PUT', 'PATCH']
        if rm in methods:
            if not request.data:
                return create_response(*type_error)
            if not all(h in header for h in header_keys):
                return create_response(*type_error)
            if not all(header[h] in header_values for h in header_keys):
                return create_response(*type_error)

        return func(*args, **kwargs)

    return decorated_function


@neighborhood_blueprint.route('/neighborhood/', methods=['POST'])
@validate_header
def get_post_rubric():
    response, status = controller.create_neighborhood(request.json, request.headers)

    return create_response(response, status)

@neighborhood_blueprint.route('/neighborhood/', methods=['GET'])
@validate_header
def get_all_neighborhoods():
    response, status = controller.get_all_neighborhoods()

    return create_response(response, status)
