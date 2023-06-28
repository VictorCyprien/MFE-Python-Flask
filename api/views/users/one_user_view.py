from typing import Dict

from flask.views import MethodView

from .users_blp import users_blp
from ...models.user import User

from ...schemas.communs_schemas import PagingError
from ...schemas.users_schemas import (
    InputUpdateUserSchema,
    UserResponseSchema
)

@users_blp.route('/<int:user_id>')
class OneUserView(MethodView):

    @users_blp.doc(operationId='GetUser')
    @users_blp.response(404, schema=PagingError, description="NotFound")
    @users_blp.response(200, schema=UserResponseSchema, description="Get one user")
    def get(self, user_id: int):
        """Get an existing user"""
        user = User.get_by_id(id=user_id)

        return {
            "user": user
        }


    @users_blp.doc(operationId='UpdateUser')
    @users_blp.arguments(InputUpdateUserSchema)
    @users_blp.response(400, schema=PagingError, description="BadRequest")
    @users_blp.response(404, schema=PagingError, description="NotFound")
    @users_blp.response(200, schema=UserResponseSchema, description="Update one user")
    def put(self, input_dict: Dict, user_id: int):
        """Update an existing user"""
        
        user = User.get_by_id(id=user_id)
        user.update(input_dict)
        user.save()

        return {
            "action": "updated",
            "user": user
        }


    @users_blp.doc(operationId='DeleteUser')
    @users_blp.response(400, schema=PagingError, description="BadRequest")
    @users_blp.response(404, schema=PagingError, description="NotFound")
    @users_blp.response(200, schema=UserResponseSchema, description="Delete one user")
    def delete(self, user_id: int):
        """Delete an existing user"""
        user = User.get_by_id(id=user_id)
        user.delete()

        return {
            "action": "deleted",
            "user": user
        }
