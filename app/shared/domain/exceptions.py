class InvalidTokenType(Exception):
    pass


class InvalidTokenStructure(Exception):
    pass


class UserNotFound(Exception):
    pass


class CreateObjectException(Exception):
    pass


class ObjectNotFound(Exception):
    def __init__(self, message: str = "Not found"):
        self.message = message
