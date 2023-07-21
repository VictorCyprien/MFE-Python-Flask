import pytest

from mongoengine.errors import DoesNotExist

from api.models.user import User

def test_model_get_user(app, victor: User, sayori: User):
    search = User.get_by_id(victor.user_id)
    assert search == victor

    search = User.get_by_id(sayori.user_id)
    assert search == sayori

    with pytest.raises(DoesNotExist):
        search = User.get_by_id(123)
