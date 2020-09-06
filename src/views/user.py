from flask import Blueprint, request
from flask_cors import CORS
from functools import wraps

from controllers import user as controller
from utils.formatters import create_response

user_blueprint = Blueprint('user', __name__, url_prefix='/api')
CORS(user_blueprint)


def validate_header(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        TYPE_ERROR = ('Unsupported media type', 415)
        header_values = ['*/*', 'application/json']
        header_keys = ['Accept', 'Content-Type']
        header = request.headers
        rm = request.method

        if rm == 'POST' or rm == 'PUT' or rm == 'PATCH':
            if not request.data:
                return create_response(*TYPE_ERROR)
            elif not all(h in header for h in header_keys):
                return create_response(*TYPE_ERROR)
            elif not all(header[h] in header_values for h in header_keys):
                return create_response(*TYPE_ERROR)

        return func(*args, **kwargs)

    return decorated_function


@user_blueprint.route('/users/', methods=['GET', 'POST'])
@validate_header
def get_post_rubric():
    if request.method == 'GET':
        response, status = controller.get_all_users()

    elif request.method == 'POST':
        response, status = controller.create_user(request.json)

    return create_response(response, status)


@user_blueprint.route('/users/<string:user_username>',
                      methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@validate_header
def user_by_username(user_username):
    if request.method == 'GET':
        response, status = controller.get_one_user(user_username)

    elif request.method == 'DELETE':
        response, status = controller.delete_user(user_username)

    elif request.method == 'PUT' or request.method == 'PATCH':
        response, status = controller.update_user(user_username, request.json)

    return create_response(response, status)
