from functools import wraps
from flask import Blueprint, request
from flask_cors import CORS

from controllers import rating as controller
from utils.formatters import create_response

from utils.validators.general import validate_header 

rating_blueprint = Blueprint('rating', __name__, url_prefix='/api')
CORS(rating_blueprint)


@rating_blueprint.route('/rating/<int:id_neighborhood>', methods=['POST'])
@validate_header
def post_rating(id_neighborhood):
    response, status = controller.create_rating(
        request.json, request.headers, id_neighborhood)

    return create_response(response, status)


@rating_blueprint.route('/rating/', methods=['GET'])
@validate_header
def get_ratings():
    response, status = controller.get_all_ratings()

    return create_response(response, status)


@rating_blueprint.route(
    '/rating/<int:id_rating>', methods=['GET', 'DELETE', 'PATCH'])
@validate_header
def rating_by_id(id_rating):
    if request.method == 'GET':
        response, status = controller.get_one_rating(id_rating)

    elif request.method == 'DELETE':
        response, status = controller.delete_rating(id_rating)

    elif request.method == 'PATCH':
        response, status = controller.update_rating(id_rating, request.json)

    return create_response(response, status)
