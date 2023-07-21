
from api.models.user import User

def test_model_update_user(app, victor: User):
    
    victor.email = "test.test@test.fr"
    
    old_password = victor._password
    victor.set_password("beedemo123")
    
    victor.save()

    new_password = victor._password

    assert victor.email == "test.test@test.fr"
    assert old_password != new_password
    