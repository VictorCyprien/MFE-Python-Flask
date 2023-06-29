from flask.app import Flask
from rich import print
from mongoengine.errors import ValidationError

from unittest.mock import ANY

from api.models.user import User


def test_create_user(client: Flask):
    data = {
        "email": "natsuki@limayrac.fr",
        "password": "beedemo",
        "name": "Natsuki"
    }

    res = client.post("/users/", json=data)
    assert res.status_code == 201
    data = res.json
    print(data)
    assert data == {
        'action': 'created',
        'user': {
            '_creation_time': ANY,
            '_update_time': ANY,
            'email': 'natsuki@limayrac.fr',
            'name': 'Natsuki',
            'scopes': ['user:member'],
            'user_id': ANY
        }
    }

    user_id = data['user']['user_id']
    user = User.objects().get(user_id=user_id)
    assert user.email == 'natsuki@limayrac.fr'
    assert user._password.startswith("$pbkdf2-sha256$")

    user.delete()


def test_create_user_empty_data(client: Flask):
    res = client.post("/users/", json={})
    assert res.status_code == 422
    data = res.json
    print(data)
    assert data == {
        'code': 422, 
        'errors': {
            'json': {
                'email': ['Missing data for required field.'], 
                'name': ['Missing data for required field.'], 
                'password': ['Missing data for required field.']
            }
        },
        'status': 'Unprocessable Entity'
    }


def test_create_user_invalid_data(client: Flask):
    res = client.post("/users/", json={"email": "", "name": " ", "password": ""})
    assert res.status_code == 422
    data = res.json
    print(data)
    assert data == {
        'code': 422,
        'errors': {'json': {'_schema': ['The email is not correct']}},
        'status': 'Unprocessable Entity'
    }


def test_create_user_invalid_email(client: Flask):
    data = {
        "email": "blabla",
        "password": "beedemo",
        "name": "TestUser"
    }

    res = client.post("/users/", json=data)
    assert res.status_code == 422
    data = res.json
    print(data)
    assert data == {
        'code': 422,
        'errors': {'json': {'_schema': ['The email is not correct']}},
        'status': 'Unprocessable Entity'
    }


def test_create_user_email_already_used(client: Flask, victor: User):
    data = {
        "email": "victor.cyprien@limayrac.fr",
        "password": "123",
        "name": "Victor"
    }

    res = client.post("/users/", json=data)
    assert res.status_code == 400
    data = res.json
    print(data)
    assert data == {
        'code': 400, 
        'message': 'This email is already used !', 
        'status': 'Bad Request'
    }
