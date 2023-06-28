from flask.app import Flask
from rich import print

from unittest.mock import ANY

from api.models.user import User

def test_delete_user(client: Flask, sayori: User):
    res = client.delete(f"/users/{sayori.user_id}")
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'action': 'deleted',
        'user': {
            '_creation_time': '2000-01-01 00:00:00',
            '_update_time': '2000-01-01 00:00:00',
            'email': 'sayori@limayrac.fr',
            'name': 'Sayori',
            'scopes': ['user:admin'],
            'user_id': ANY
        }
    }


def test_delete_user_not_found(client: Flask):
    res = client.delete("/users/123456789")
    assert res.status_code == 404
    data = res.json
    print(data)
    assert data == {
        'code': 404, 
        'message': 'User #123456789 not found !', 
        'status': 'Not Found'
    }


def test_delete_user_two_times(client: Flask, sayori: User):
    res = client.delete(f"/users/{sayori.user_id}")
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'action': 'deleted',
        'user': {
            '_creation_time': '2000-01-01 00:00:00',
            '_update_time': '2000-01-01 00:00:00',
            'email': 'sayori@limayrac.fr',
            'name': 'Sayori',
            'scopes': ['user:admin'],
            'user_id': ANY
        }
    }

    res = client.delete(f"/users/{sayori.user_id}")
    assert res.status_code == 404
    data = res.json
    print(data)
    assert data == {}
