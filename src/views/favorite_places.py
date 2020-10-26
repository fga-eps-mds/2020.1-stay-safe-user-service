from flask import Blueprint, request
from flask_cors import CORS

from controllers import favorite_places as controller
from utils.formatters import create_response

from utils.validators.general import validate_header, validate_token

favorite_places_blueprint = Blueprint('favorite_places', __name__, url_prefix='/api')
CORS(favorite_places_blueprint)


@favorite_places_blueprint.route('/places/', methods=['POST'])
@validate_header
@validate_token
def post_favorite_place(username):
    response, status = controller.create_favorite_place(
        request.json, username)

    return create_response(response, status)

@favorite_places_blueprint.route('/places/<int:id_place>', methods=['DELETE'])
@validate_header
@validate_token
def delete_favorite_place_by_id(username, id_place):
    response, status = controller.delete_favorite_place(username, id_place)

    return create_response(response, status)

@favorite_places_blueprint.route('/places/', methods=['GET'])
@validate_header
@validate_token
def get_favorite_places_by_user(username):
    response, status = controller.get_favorite_places(username)

    return create_response(response, status)
