from flask.app import Flask
from rich import print

from api.models.user import User

def test_get_users(client: Flask, victor: User, sayori: User):
    res = client.get("/users/")
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'users': [
            {
                '_creation_time': '2000-01-01 00:00:00',
                '_update_time': '2000-01-01 00:00:00',
                'email': 'victor.cyprien@limayrac.fr',
                'name': 'Victor CYPRIEN',
                'scopes': ['user:admin'],
                'user_id': victor.user_id
            },
            {
                '_creation_time': '2000-01-01 00:00:00',
                '_update_time': '2000-01-01 00:00:00',
                'email': 'sayori@limayrac.fr',
                'name': 'Sayori',
                'scopes': ['user:admin'],
                'user_id': sayori.user_id
            }
        ]
    }

def test_get_one_user(client: Flask, victor: User):
    res = client.get(f"/users/{victor.user_id}")
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'user': {
            '_creation_time': '2000-01-01 00:00:00',
            '_update_time': '2000-01-01 00:00:00',
            'email': 'victor.cyprien@limayrac.fr',
            'name': 'Victor CYPRIEN',
            'scopes': ['user:admin'],
            'user_id': victor.user_id
        }
    }


def _test_get_one_user_not_found(client: Flask, victor: User):
    res = client.get("/users/123")
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'user': {
            '_creation_time': '2000-01-01 00:00:00',
            '_update_time': '2000-01-01 00:00:00',
            'email': 'victor.cyprien@limayrac.fr',
            'name': 'Victor CYPRIEN',
            'scopes': ['user:admin'],
            'user_id': victor.user_id
        }
    }
