from flask import Flask
from flask_cors import CORS

from settings import logger, load_configuration
from views.user import user_blueprint
from views.auth import auth_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(auth_blueprint)

CORS(app, automatic_options=True)


if __name__ == '__main__':
    server_config = load_configuration()
    logger.info(f"Service configurations: {server_config}")

    logger.info("User service initialized and ready to use!\n")

    app.run(**server_config)
