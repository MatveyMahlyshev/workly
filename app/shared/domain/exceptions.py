class InvalidTokenType(Exception):
    pass


class InvalidTokenStructure(Exception):
    pass


class UserNotFound(Exception):
    pass


class CreateObjectException(Exception):
    def __init__(self, message: str = "Server error"):
        self.message = message


class UniqueException(Exception):
    def __init__(self, message: str):
        self.message = message


class ObjectNotFound(Exception):
    def __init__(self, message: str = "Not found"):
        self.message = message


class ObjectUpdateError(Exception):
    pass
