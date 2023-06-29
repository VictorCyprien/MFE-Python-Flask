from flask.app import Flask
from rich import print

from unittest.mock import ANY

from api.models.user import User

def test_user_update(client: Flask, victor: User):
    data_put = {
        "email": "vic.vic@vic.fr",
        "name": "Vic",
        "password": "vic123456"
    }

    res = client.put(f"/users/{victor.user_id}", json=data_put)
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'action': 'updated',
        'user': {
            '_creation_time': '2000-01-01 00:00:00',
            '_update_time': ANY,
            'email': 'vic.vic@vic.fr',
            'name': 'Vic',
            'scopes': ['user:admin'],
            'user_id': ANY
        }
    }


def _test_user_update_not_admin(client: Flask, victor: User, sayori: User):
    victor.scopes = ["user:member"]
    victor.save()

    data_put = {
        "email": "sayori@limayrac.fr"
    }

    res = client.put(f"/users/{sayori.user_id}", json=data_put)
    assert res.status_code == 404
    data = res.json
    print(data)
    assert data == {
        'code': 404, 
        'message': f'User #{sayori.user_id} not found !', 
        'status': 'Not Found'
    }


def _test_user_update_email_already_used(client: Flask, victor: User, sayori: User):
    data_put = {
        "email": sayori.email
    }

    res = client.put(f"/users/{victor.user_id}", json=data_put)
    assert res.status_code == 400
    data = res.json
    print(data)
    assert data == {
        'code': 400,
        'message': 'An error has occured during profil update, please try again',
        'status': 'Bad Request'
    }


def _test_user_update_email_invalid_email(client: Flask, victor: User, sayori: User):
    data_put = {
        "email": "blabla"
    }

    res = client.put(f"/users/{victor.user_id}", json=data_put)
    assert res.status_code == 400
    data = res.json
    print(data)
    assert data == {
        'code': 400, 
        'message': 'This email is invalid', 
        'status': 'Bad Request'
    }


def _test_user_update_not_found(client: Flask, victor: User):
    data_put = {
        "email": "vic.vic@vic.fr",
        "name": "Vic",
        "password": "vic123456"
    }

    res = client.put("/users/86489686484864", json=data_put)
    assert res.status_code == 404
    data = res.json
    print(data)
    assert data == {
        'code': 404,
        'message': 'User #86489686484864 not found !',
        'status': 'Not Found'
    }
