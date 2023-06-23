from flask.app import Flask
from rich import print

from unittest.mock import ANY

from api.models.user import User

def test_get_users(client: Flask, victor: User, tristan: User):
    res = client.get("/users/")
    assert res.status_code == 200
    data = res.json
    print(data)
    assert data == {
        'users': [
            {
                '_creation_time': '2000-01-01 00:00:00',
                '_last_login': ANY,
                '_update_time': '2000-01-01 00:00:00',
                'email': 'victor.cyprien@barbuc.fr',
                'name': 'Victor CYPRIEN',
                'scopes': ['user:admin'],
                'user_id': ANY
            },
            {
                '_creation_time': '2000-01-01 00:00:00',
                '_last_login': ANY,
                '_update_time': '2000-01-01 00:00:00',
                'email': 'tristan.calvet@barbuc.fr',
                'name': 'Tristan CALVET',
                'scopes': ['user:admin'],
                'user_id': ANY
            }
        ]
    }
