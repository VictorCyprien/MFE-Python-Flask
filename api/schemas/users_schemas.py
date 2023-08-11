from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow.validate import Range

from ..models.user import USER_ID_MAX_VAL, User

class UserSchema(Schema):
    user_id = fields.Integer(
        attribute='user_id',
        validate=Range(min=0, min_inclusive=False, max=USER_ID_MAX_VAL, max_inclusive=False),
        metadata={"description": "Unique user identifier"}
    )
    name = fields.String(metadata={"description": "Name of the user"})
    email = fields.String(metadata={"description": "Email of the user"})
    scopes = fields.List(fields.String, metadata={"description": "Scopes of the user"})
    
    _creation_time = fields.String(
        format="date-time",
        allow_none=True,
        data="creation_time",
        metadata={"description": "User creation time"}
    )

    _update_time = fields.String(
        format="date-time",
        allow_none=True,
        data="update_time",
        metadata={"description": "Last user update time"}
    )

    class Meta:
        ordered = True
        description = "User informations."


class UserResponseSchema(Schema):
    action = fields.String()
    user = fields.Nested(UserSchema)

    class Meta:
        ordered = True
        description = "Create/Update/Delete a user."


class GetUsersListSchema(Schema):
    users = fields.Nested(UserSchema, many=True)

    class Meta:
        description = "List of users."
        ordered = True


class InputCreateUserSchema(Schema):
    user_id = fields.Integer(
        validate=Range(
            min=1, 
            error="The user_id is incorrect. It must be greater than 0"
        ),
        metadata={"description": "ID of the User"}
    )
    email = fields.String(metadata={"description": "Email of the user"}, required=True)
    password = fields.String(metadata={"description": "Password of the user"}, required=True)
    name = fields.String(metadata={"description": "Name of the user"}, required=True)
    scopes = fields.List(
        fields.String,
        metadata={"description": "Scopes of the user"},
        required=False
    )

    @validates_schema
    def validation_payload(self, data, **kwargs):
        email: str = data["email"]
        name: str = data["name"]
        password: str = data["password"]

        if not email.strip() or not User.isValidEmail(email):
            raise ValidationError("The email is not correct")
        
        if not name.strip():
            raise ValidationError("The name is empty")

        if not password.strip():
            raise ValidationError("The password is empty")

    class Meta:
        description = "Input informations need to create user."
        ordered = True


class InputUpdateUserSchema(Schema):
    email = fields.String(metadata={"description": "New email of the user"}, required=False)
    password = fields.String(metadata={"description": "New password of the user"}, required=False)
    name = fields.String(metadata={"description": "New name of the user"}, required=False)
    scopes = fields.List(
        fields.String,
        metadata={"description": "New scopes of the user"},
        required=False
    )

    @validates_schema
    def validation_payload(self, data, **kwargs):
        email: str = data.get("email", None)

        if email is None:
            return

        if not email.strip() or not User.isValidEmail(email):
            raise ValidationError("The email is not correct")

    class Meta:
        description = "New user information"
        ordered = True
