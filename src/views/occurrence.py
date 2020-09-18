from flask import Blueprint, request
from flask_cors import CORS

from controllers import occurrence as controller
from utils.formatters import create_response
from utils.validators.general import validate_header

occurrence_blueprint = Blueprint('occurrence', __name__, url_prefix='/api')
CORS(occurrence_blueprint)


@occurrence_blueprint.route('/occurrences/', methods=['GET', 'POST'])
@validate_header
def get_post_rubric():
    if request.method == 'GET':
        response, status = controller.get_all_occurrences()

    elif request.method == 'POST':
        response, status = controller.create_occurrence(request.json,
                                                        request.headers)

    return create_response(response, status)


@occurrence_blueprint.route('/occurrences/<int:occurrence_id>',
                            methods=['GET', 'PATCH', 'DELETE'])
@validate_header
def occurrence_by_id(occurrence_id):
    if request.method == 'GET':
        response, status = controller.get_one_occurrence(occurrence_id)

    elif request.method == 'DELETE':
        response, status = controller.delete_occurrence(occurrence_id)

    elif request.method == 'PATCH':
        response, status = controller.update_occurrence(occurrence_id,
                                                        request.json)

    return create_response(response, status)
