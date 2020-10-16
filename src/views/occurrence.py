from flask import Blueprint, request
from flask_cors import CORS

from controllers import occurrence as controller
from utils.formatters import create_response
from utils.validators.general import validate_header, validate_token

from settings import logger

occurrence_blueprint = Blueprint('occurrence', __name__, url_prefix='/api')
CORS(occurrence_blueprint)


@occurrence_blueprint.route('/occurrences/', methods=['POST'])
@validate_header
@validate_token
def post_occurrence(username):
    response, status = controller.create_occurrence(username, request.json)

    return create_response(response, status)


@occurrence_blueprint.route('/occurrences/', methods=['GET'])
def get_all_occurrences():
    user = request.args.get('user')
    occurrence_type = request.args.get('occurrence_type')

    response, status = controller.get_all_occurrences(user, occurrence_type)

    return create_response(response, status)


@occurrence_blueprint.route('/occurrences/<int:occurrence_id>',
                            methods=['GET'])
def occurrence_by_id(occurrence_id):
    response, status = controller.get_one_occurrence(occurrence_id)

    return create_response(response, status)


@occurrence_blueprint.route('/occurrences/<int:occurrence_id>',
                            methods=['PATCH', 'DELETE'])
@validate_header
@validate_token
def delete_patch_occurrence(username, occurrence_id):
    logger.info("#########")
    logger.info(occurrence_id)
    if request.method == 'DELETE':
        response, status = controller.delete_occurrence(occurrence_id)

    elif request.method == 'PATCH':
        response, status = controller.update_occurrence(occurrence_id,
                                                        request.json)

    return create_response(response, status)
