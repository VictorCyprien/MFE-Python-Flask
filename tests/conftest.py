
from typing import Iterator
from flask import Flask
from flask import testing
from flask.testing import FlaskClient

from werkzeug.datastructures import Headers

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


class TestClient(testing.FlaskClient):
    global_headers = {}
    def open(self, *args, **kwargs):
        api_key_headers = Headers(self.global_headers)
        headers = kwargs.pop('headers', {})
        if not isinstance(headers, Headers):
            headers = Headers(headers)
        headers.extend(api_key_headers)
        kwargs['headers'] = headers
        return super().open(*args, **kwargs)


@pytest.fixture(scope='module')
def client(app: Flask) -> Iterator[TestClient]:
    app.test_client_class = TestClient
    client = app.test_client()
    yield client


def _raz_auth_headers(client: TestClient):
    client.global_headers = {}


@pytest.fixture(scope='function')
def client_victor(client: TestClient, victor: User) -> Iterator[FlaskClient]:
    yield client
    _raz_auth_headers(client)


@pytest.fixture(scope='function')
def client_tristan(client: TestClient, tristan: User) -> Iterator[FlaskClient]:
    yield client
    _raz_auth_headers(client)


@pytest.fixture(scope='function')
def client_member(client: TestClient, member: User) -> Iterator[FlaskClient]:
    yield client
    _raz_auth_headers(client)


#### USERS ####

creation_date = '2000-01-01T00:00:00+00:00'

@pytest.fixture(scope='function')
def victor(app) -> Iterator[User]:
    #  victor is "admin"
    user_dict = {
        "email": "victor.cyprien@barbuc.fr",
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
def tristan(app) -> Iterator[User]:
    #  tristan is "admin"
    user_dict = {
        "email": "tristan.calvet@barbuc.fr",
        "name": "Tristan CALVET",
        "password": "beedemo"
    }
    with freezegun.freeze_time(creation_date):
        user = User.create(user_dict)
        user.scopes = ["user:admin"]
        user.save()
    yield user
    user.delete()


@pytest.fixture(scope='function')
def member(app) -> Iterator[User]:
    #  member is not "admin"
    user_dict = {
        "email": "member1@barbuc.fr",
        "name": "Member 1",
        "password": "beedemo"
    }
    with freezegun.freeze_time(creation_date):
        user = User.create(user_dict)
        user.save()
    yield user
    user.delete()


#### MOCKS ####

@pytest.fixture
def mock_save_user_document():
    from api.models.user import User
    from mongoengine.errors import ValidationError
    _original = User.save
    User.save = Mock()
    User.save.side_effect = ValidationError
    yield User.save
    User.save = _original
