from flask import Blueprint, request
from flask_cors import CORS

from controllers import notifications as controller
from utils.formatters import create_response
from settings import logger
from utils.validators.general import validate_header, validate_token

notifications_blueprint = Blueprint(
    'notifications', __name__, url_prefix='/api')


@notifications_blueprint.route('/notification-places/', methods=['POST'])
@validate_header
@validate_token
def post_send_notifications(username):
    response, status = controller.send_notifications_near_occcurrences(
        request.json, username
    )

    return create_response(response, status)
