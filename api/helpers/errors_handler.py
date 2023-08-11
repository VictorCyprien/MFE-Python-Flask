from werkzeug.exceptions import BadRequest as WerkzeugBadRequest
from werkzeug.exceptions import NotFound as WerkzeugNotFound
from enum import Enum


class BadRequest(WerkzeugBadRequest):
    """ BadRequest error customized for default smorest error handler

    >>> err = BadRequest("An important message")
    >>> err.data
    {'message': 'An important message'}
    """
    def __init__(self, message: str = None) -> None:
        super().__init__()
        if message:
            self.data = {}
            self.data["message"] = message


class NotFound(WerkzeugNotFound):
    """ NotFound error customized for default smorest error handler

    >>> err = NotFound("An important message")
    >>> err.data
    {'message': 'An important message'}
    """
    def __init__(self, message: str = None) -> None:
        super().__init__()
        if message:
            self.data = {}
            self.data["message"] = message


class ErrorHandler(Enum):
    USER_NOT_FOUND = "This user doesn't exist !"
    EMAIL_ALREADY_USED = "This email is already used !"
    UPDATE_USER_ERROR = "Something went wrong when updating the user, please try again !"
