from mongoengine import Document, fields
from mongoengine.errors import ValidationError

from passlib.handlers.pbkdf2 import pbkdf2_sha256

from datetime import datetime

import pytz
import re
import random

from ..config import config

USER_ID_MAX_VAL = 2**31-1


class User(Document):
    user_id: int = fields.IntField(db_field="user_id", min_value=0, max_value=USER_ID_MAX_VAL, required=True, primary_key=True)
    """ ID of the User
    """

    email: str = fields.StringField(required=True, unique=True)
    """ Email address of the User
    """

    name: str = fields.StringField(required=True)
    """ Username of the user (ex "Victor")
    """

    _password: str = fields.StringField(db_field="password")
    """ Password of the User (Hash of the user's password)
    """

    _creation_time = fields.DateTimeField(db_field="creation_time")
    """ Creation time of the User
    """

    _update_time = fields.DateTimeField(db_field="update_time")
    """ Last time action of the User
    """

    scopes = fields.ListField(fields.StringField(), default=None)
    """ Permissions of the User
    """


    @property
    def creation_time(self):
        return self._creation_time

    @creation_time.setter
    def creation_time(self, time):
        self._creation_time = time

    @property
    def update_time(self):
        return self._update_time if self._update_time is not None else None

    @update_time.setter
    def update_time(self, time):
        self._update_time = time

    @classmethod
    def create(cls, input_data: dict) -> "User":
        """ Create a new user instance
        """
        user = User()
        password = None
        if 'user_id' not in input_data:
            input_data['user_id'] = cls._next_id()
        if 'password' in input_data:
            password = input_data['password']
            del input_data['password']
        if 'email' in input_data:
            email = input_data['email']
            del input_data['email']
        if 'name' in input_data:
            name = input_data['name']
            del input_data['name']

        user.user_id = input_data['user_id']
        user.email = email
        user.name = name
        user.scopes = ["user:member"]

        if password is not None:
            user.set_password(password)  
        # Set creation time
        user.creation_time = datetime.now(tz=pytz.utc).replace(microsecond=0)
        user.update_time = datetime.now(tz=pytz.utc).replace(microsecond=0)
        return user

    
    def update(self, input_data: dict):
        """ Update the current instance of a User
        """
        if "email" in input_data:
            new_email = input_data["email"]
            self.email = new_email
        if "password" in input_data:
            new_password = input_data["password"]
            self.set_password(new_password)
        if "name" in input_data:
            new_name = input_data["name"]
            self.name = new_name
        if "scopes" in input_data:
            new_scopes = input_data["scopes"]
            self.scopes = new_scopes
        self.update_time = datetime.now(tz=pytz.utc).replace(microsecond=0)


    def set_password(self, password: str):
        salt = config.SECURITY_PASSWORD_SALT.encode('utf8')
        self._password = pbkdf2_sha256.using(salt=salt).hash(password)
        self.update_time = datetime.now(tz=pytz.utc).replace(microsecond=0)

    
    @staticmethod
    def isValidEmail(email: str) -> bool:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.fullmatch(regex, email)


    @classmethod
    def _next_id(cls) -> int:
        user_id = random.randint(0, USER_ID_MAX_VAL)
        nb_trial = 0
        while cls.objects(pk=user_id).count() and nb_trial < 10:
            user_id = random.randint(0, USER_ID_MAX_VAL)
            nb_trial += 1
        if nb_trial > 10:
            raise RuntimeError("Impossible to get new user id")
        return user_id


    @classmethod
    def get_by_id(cls, id: int) -> "User":
        """ User getter with a ID
        """
        try:
            user_id = int(id)
        except ValueError:
            raise ValidationError('The user ID should be an int')
        _query = User.objects(user_id=user_id)
        user = _query.get()
        return user
