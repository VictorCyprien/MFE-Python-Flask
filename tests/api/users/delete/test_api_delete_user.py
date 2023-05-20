from flask.app import Flask
from rich import print

from unittest.mock import ANY

from api.models.user import User

def test_delete_user(client: Flask, victor: User, tristan: User):
    res = client.delete(f"/users/{tristan.user_id}")
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'action': 'deleted',
        'user': {
            '_creation_time': '2000-01-01 00:00:00',
            '_last_login': ANY,
            '_update_time': '2000-01-01 00:00:00',
            'email': 'tristan.calvet@barbuc.fr',
            'name': 'Tristan CALVET',
            'scopes': ['user:admin'],
            'user_id': ANY
        }
    }


def test_delete_user_not_admin(client: Flask, victor: User, tristan: User):
    victor.scopes = ["user:member"]
    victor.save()

    res = client.delete(f"/users/{tristan.user_id}")
    assert res.status_code == 404
    data = res.json
    print(data)
    assert data == {
        'code': 404, 
        'message': f'User #{tristan.user_id} not found !', 
        'status': 'Not Found'
    }


def test_delete_user_himself(client: Flask, victor: User):
    victor.scopes = ["user:member"]
    victor.save()

    res = client.delete(f"/users/{victor.user_id}")
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'action': 'deleted',
        'user': {
            '_creation_time': '2000-01-01 00:00:00',
            '_last_login': ANY,
            '_update_time': '2000-01-01 00:00:00',
            'email': 'victor.cyprien@barbuc.fr',
            'name': 'Victor CYPRIEN',
            'scopes': ['user:member'],
            'user_id': ANY
        }
    }


def test_delete_user_not_found(client: Flask, victor: User, tristan: User):
    res = client.delete("/users/123456789")
    assert res.status_code == 404
    data = res.json
    print(data)
    assert data == {
        'code': 404, 
        'message': 'User #123456789 not found !', 
        'status': 'Not Found'
    }


def test_delete_user_two_times(client: Flask, member: User):
    res = client.delete(f"/users/{member.user_id}")
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'action': 'deleted',
        'user': {
            '_creation_time': '2000-01-01 00:00:00',
            '_last_login': ANY,
            '_update_time': '2000-01-01 00:00:00',
            'email': 'member1@barbuc.fr',
            'name': 'Member 1',
            'scopes': ['user:member'],
            'user_id': ANY
        }
    }

    res = client.delete(f"/users/{member.user_id}")
    assert res.status_code == 404
    data = res.json
    print(data)
    assert data == {}
