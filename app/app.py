import json
import sys
import logging.config
import click
from environs import Env

from urllib.parse import urlparse

from flask import Flask, request, jsonify
from flask_compress import Compress
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_smorest import Api
from flask.cli import AppGroup
from flask_wtf.csrf import CSRFProtect

from .config import Config


def create_flask_app(config: Config) -> Flask:
    # Create the Flask App
    app = Flask(__name__)
    app.config["WTF_CSRF_CHECK_DEFAULT"] = True
    app.config['CORS_HEADERS'] = 'Content-Type'

    csrf = CSRFProtect()
    csrf.init_app(app)

    CORS(app, resources={r"/foo": {"origins": "https://localhost:port"}})
    Compress(app)

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

    # Log the current conf
    cname = env.str('CI_COMMIT_REF_NAME', None)
    csha = env.str('CI_COMMIT_SHA', None)
    if cname:
        app.logger.info(f"Current commit name: {cname}")
    if csha:
        app.logger.info(f"Current commit sha: {csha}")

    app.debug = config.FLASK_ENV

    # Configure mongo client
    app.mongo_client = MongoEngine(app=app)

    #Add healthcheck
    # health = HealthCheck(app, "/healthcheck")
    # health.add_check(mongo_available())

    # Index routes
    # @app.route('/')
    # def index(authenticated_user: User):
    #     res = {
    #         'name': config.SERVICE_NAME,
    #         'commit_name': cname,
    #         'commit_sha': csha,
    #         'user_id': authenticated_user.user_id,
    #     }
    #     return jsonify(res)
    # 

    @app.route("/")
    def index():
        return "Hello World !"

    # from .views.users import users_blp
    # rest_api.register_blueprint(users_blp)

    app.logger.debug(f"URL Map: \n{app.url_map}")
    return app
