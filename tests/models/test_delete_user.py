from api.models.user import User

def test_model_delete_user(app, victor: User):
    victor.delete()
    assert victor is not User
