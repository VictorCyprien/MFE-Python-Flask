
from typing import Iterator
from flask import Flask
from flask.testing import FlaskClient

from mongoengine.connection import disconnect
from unittest.mock import Mock
import pytest
import freezegun

from api.models.user import User


@pytest.fixture(scope='session')
def app(request) -> Iterator[Flask]:
    """ Session-wide test `Flask` application. """
    disconnect()    # force close potential existing mongo connection
    from api.config import config
    config.MONGODB_URI = "mongomock://localhost"
    config.MONGODB_DATABASE = "test"
    config.MONGODB_CONNECT = False

    config.SECURITY_PASSWORD_SALT = "123456"

    from api.app import create_flask_app
    _app = create_flask_app(config=config)
    yield _app


@pytest.fixture(scope='module')
def client(app: Flask) -> Iterator[FlaskClient]:
    app.test_client_class = FlaskClient
    client = app.test_client()
    yield client

#### USERS ####

creation_date = '2000-01-01T00:00:00+00:00'

@pytest.fixture(scope='function')
def victor(app) -> Iterator[User]:
    #  victor is "admin"
    user_dict = {
        "email": "victor.cyprien@limayrac.fr",
        "name": "Victor CYPRIEN",
        "password": "beedemo"
    }
    with freezegun.freeze_time(creation_date):
        user = User.create(user_dict)
        user.scopes = ["user:admin"]
        user.save()
    yield user
    user.delete()


@pytest.fixture(scope='function')
def sayori(app) -> Iterator[User]:
    #  sayori is "admin"
    user_dict = {
        "email": "sayori@limayrac.fr",
        "name": "Sayori",
        "password": "beedemo"
    }
    with freezegun.freeze_time(creation_date):
        user = User.create(user_dict)
        user.scopes = ["user:admin"]
        user.save()
    yield user
    user.delete()
