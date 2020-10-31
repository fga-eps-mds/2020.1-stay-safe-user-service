from flask import Blueprint, request
from flask_cors import CORS

from controllers import rating as controller
from utils.formatters import create_response

from utils.validators.general import validate_header, validate_token

rating_blueprint = Blueprint('rating', __name__, url_prefix='/api')
CORS(rating_blueprint)


@rating_blueprint.route('/rating/<int:id_neighborhood>', methods=['POST'])
@validate_header
@validate_token
def post_rating(username, id_neighborhood):
    response, status = controller.create_rating(
        request.json, username, id_neighborhood)

    return create_response(response, status)


@rating_blueprint.route('/rating/', methods=['GET'])
def get_ratings():
    user = request.args.get('user')
    neighborhood = request.args.get('neighborhood')

    response, status = controller.get_all_ratings(user, neighborhood)

    return create_response(response, status)


@rating_blueprint.route(
    '/rating/<int:id_rating>', methods=['GET'])
def get_rating_by_id(id_rating):
    response, status = controller.get_one_rating(id_rating)

    return create_response(response, status)


@rating_blueprint.route(
    '/rating/<int:id_rating>', methods=['DELETE', 'PATCH'])
@validate_header
@validate_token
def rating_by_id(username, id_rating):
    if request.method == 'DELETE':
        response, status = controller.delete_rating(id_rating, username)

    elif request.method == 'PATCH':
        response, status = controller.update_rating(id_rating, request.json, username)

    return create_response(response, status)
