import logging

from flask.views import MethodView
from mongoengine.errors import NotUniqueError, ValidationError

from .users_blp import users_blp
from ...models.user import User

from ...schemas.communs_schemas import PagingError
from ...schemas.users_schemas import (
    GetUsersListSchema,
    InputCreateUserSchema,
    UserResponseSchema
)

from ...helpers.errors_handler import BadRequest, ErrorHandler

logger = logging.getLogger('console')


@users_blp.route('/')
class RootUsersView(MethodView):

    @users_blp.doc(operationId='ListUsers')
    @users_blp.response(200, schema=GetUsersListSchema, description="List of users found in the database")
    def get(self):
        users = User.objects()
        
        return {
            'users': users,
        }

    @users_blp.doc(operationId='CreateUser')
    @users_blp.arguments(InputCreateUserSchema)
    @users_blp.response(400, schema=PagingError, description="BadRequest")
    @users_blp.response(201, schema=UserResponseSchema, description="Infos of new user")
    def post(self, input_data: dict):
        """Create a new user"""
        user = User.create(input_data=input_data)

        try:
            user.save()
        except NotUniqueError:
            raise BadRequest(ErrorHandler.EMAIL_ALREADY_USED.value)

        return {
            'action': 'created',
            'user': user
        }
