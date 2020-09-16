from functools import wraps
from flask import Blueprint, request
from flask_cors import CORS

from controllers import rating as controller
from utils.formatters import create_response

rating_blueprint = Blueprint('rating', __name__, url_prefix='/api')
CORS(rating_blueprint)


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


@rating_blueprint.route('/rating/<int:id_neighborhood>', methods=['POST'])
@validate_header
def post_rating(id_neighborhood):
    response, status = controller.create_rating(request.json, request.headers, id_neighborhood)

    return create_response(response, status)

@rating_blueprint.route('/rating/', methods=['GET'])
@validate_header 
def get_ratings():
    response, status = controller.get_all_ratings()

    return create_response(response, status)

@rating_blueprint.route('/rating/<int:id_rating>', methods=['GET'])
@validate_header
def rating_by_id(id_rating):
    response, status = controller.get_one_rating(id_rating)

    return create_response(response, status)
    