from api.models.user import User

def test_model_create_user(app):

    user_data = {
        "email": "victor.cyprien@limayrac.fr",
        "password": "beedemo123",
        "name": "Victor CYPRIEN",
    }

    user = User().create(input_data=user_data)
    
    assert user.email == "victor.cyprien@limayrac.fr"
    assert user._password.startswith('$pbkdf2-sha256')
    assert user.name == "Victor CYPRIEN"
    assert user.scopes == ['user:member']
