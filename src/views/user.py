from flask import Blueprint, request
from flask_cors import CORS

from controllers import user as controller
from utils.formatters import create_response

user_blueprint = Blueprint('user', __name__, url_prefix='/api')
CORS(user_blueprint)


@user_blueprint.route('/users/', methods=['GET', 'POST'])
def get_post_rubric():
    if request.method == 'GET':
        response, status = controller.get_all_users()

    elif request.method == 'POST':
        response, status = controller.create_user(request.json)

    return create_response(response, status)


@user_blueprint.route('/users/<string:user_username>',
                      methods=['GET', 'PUT', 'DELETE'])
def user_by_username(user_username):
    if request.method == 'GET':
        response, status = controller.get_one_user(user_username)

    elif request.method == 'DELETE':
        response, status = controller.delete_user(user_username)

    return create_response(response, status)
