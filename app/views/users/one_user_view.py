from typing import Dict
import logging

from flask.views import MethodView

from .users_blp import users_blp
from ...models.user import User


logger = logging.getLogger('console')


@users_blp.route('/<int:user_id>')
class OneUserView(MethodView):

    @users_blp.doc(operationId='GetUser')
    def get(self, user_id: int):
        """Get an existing user"""
        user = User.get_by_id(id=user_id)

        return {
            "action": "updated",
            "user": user
        }


    @users_blp.doc(operationId='UpdateUser')
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
    def delete(self, user_id: int):
        """Delete an existing user"""
        user = User.get_by_id(id=user_id)
        user.delete()

        return {
            "action": "deleted",
            "user": user
        }
