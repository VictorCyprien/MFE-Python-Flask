import json
import logging.config
from environs import Env

from flask import Flask, request, jsonify
from flask_smorest import Api

from .config import Config


def create_flask_app(config: Config) -> Flask:
    # Create the Flask App
    app = Flask(__name__)
    app.logger = logging.getLogger('console')

    """ Log each API/APP request
    """

    @app.before_request
    def before_request():
        """ Log every requests """
        app.logger.info(f'>-- {request.method} {request.path} from {request.remote_addr}')
        app.logger.debug(f'       Args: {request.args.to_dict()}')
        app.logger.debug(f'    Headers: {request.headers.to_wsgi_list()}')
        app.logger.debug(f'       Body: {request.get_data()}')

    @app.after_request
    def after_request(response):
        """ Log response status, after every request. """
        app.logger.info(f'--> Response status: {response.status}')
        app.logger.debug(f'      Body: {response.json}')
        return response

    env = Env()

    app.logger.info('.------------------.')
    app.logger.info('| MFE Python-Flask|')
    app.logger.info('.------------------.')

    # Update config from given one
    app.config.update(**config.json)
    app.logger.info(f"Config: {json.dumps(config.json, indent=4)}")
    app.debug = config.FLASK_ENV

    # Configure mongo client
    from mongoengine import connect
    connect(config.MONGODB_DATABASE, host=config.MONGODB_URI)

    # Index routes
    @app.route('/')
    def index():
        res = {
            'name': config.SERVICE_NAME,
        }
        return jsonify(res)
    

    rest_api = Api(app)

    from .views.users import users_blp
    rest_api.register_blueprint(users_blp)

    app.logger.debug(f"URL Map: \n{app.url_map}")
    return app
