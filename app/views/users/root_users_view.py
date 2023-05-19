import logging

from flask.views import MethodView
from mongoengine.errors import NotUniqueError, ValidationError

from .users_blp import users_blp
from ...models.user import User


logger = logging.getLogger('console')


@users_blp.route('/')
class RootUsersView(MethodView):

    @users_blp.doc(operationId='ListUsers')
    def get(self):
        users = User.objects()

        return {
            'users': users,
        }


    @users_blp.doc(operationId='CreateUser')
    def post(self, input_data: dict):
        """Create a new user"""
        user = User.create(input_data=input_data)
        user.save()

        return {
            'action': 'created',
            'user': user
        }
