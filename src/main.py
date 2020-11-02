from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from settings import logger, load_configuration
from views.user import user_blueprint
from views.occurrence import occurrence_blueprint
from views.auth import auth_blueprint
from views.neighborhood import neighborhood_blueprint
from views.rating import rating_blueprint
from views.favorite_places import favorite_places_blueprint

swagger_blueprint = get_swaggerui_blueprint(
    '/api/docs',
    '/static/swagger.json',
    config={
        'app_name': "User Service - Stay Safe"
    }
)

app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(occurrence_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(neighborhood_blueprint)
app.register_blueprint(rating_blueprint)
app.register_blueprint(favorite_places_blueprint)
app.register_blueprint(swagger_blueprint, url_prefix='/api/docs')

CORS(app, automatic_options=True)

if __name__ == '__main__':
    server_config = load_configuration()
    logger.info(f"Service configurations: {server_config}")

    logger.info("User service initialized and ready to use!\n")

    app.run(**server_config)
