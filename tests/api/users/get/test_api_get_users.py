from flask.app import Flask
from rich import print

from unittest.mock import ANY

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
                'user_id': ANY
            },
            {
                '_creation_time': '2000-01-01 00:00:00',
                '_update_time': '2000-01-01 00:00:00',
                'email': 'sayori@limayrac.fr',
                'name': 'Sayori',
                'scopes': ['user:admin'],
                'user_id': ANY
            }
        ]
    }
