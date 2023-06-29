from werkzeug.exceptions import BadRequest as WerkzeugBadRequest
from werkzeug.exceptions import NotFound as WerkzeugNotFound


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
