from flask import Blueprint, request
from flask_cors import CORS

from controllers import neighborhood as controller
from utils.formatters import create_response

from utils.validators.general import validate_header

neighborhood_blueprint = Blueprint('neighborhood', __name__, url_prefix='/api')
CORS(neighborhood_blueprint)


@neighborhood_blueprint.route('/neighborhood/', methods=['POST'])
@validate_header
def get_post_rubric():
    response, status = controller.create_neighborhood(
        request.json)

    return create_response(response, status)


@neighborhood_blueprint.route('/neighborhood/', methods=['GET'])
@validate_header
def get_all_neighborhoods():
    response, status = controller.get_all_neighborhoods()

    return create_response(response, status)


@neighborhood_blueprint.route(
    '/neighborhood/<int:id_neighborhood>', methods=['GET', 'DELETE'])
@validate_header
def delete_get_neighborhood(id_neighborhood):
    if request.method == 'DELETE':
        response, status = controller.delete_neighborhood(id_neighborhood)
    elif request.method == 'GET':
        response, status = controller.get_one_neighborhood(id_neighborhood)

    return create_response(response, status)
