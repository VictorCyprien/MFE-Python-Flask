from api.models.user import User

def test_model_update_user(app, victor: User):
    data_update = {
        "email": "victor.cyprien123@limayrac.fr",
        "password": "beedemo456",
        "name": "CYPRIEN Victor",
        "scopes": ["user:member"]
    }

    assert victor.email == "victor.cyprien@limayrac.fr"
    assert victor.name == "Victor CYPRIEN"
    assert victor.scopes == ["user:admin"]

    victor.update(input_data=data_update)
    victor.save()
    victor.reload()

    assert victor.email != "victor.cyprien@limayrac.fr" and victor.email == "victor.cyprien123@limayrac.fr"
    assert victor.name != "Victor CYPRIEN" and victor.name == "CYPRIEN Victor"
    assert victor.scopes != ["user:admin"] and victor.scopes == ["user:member"]
