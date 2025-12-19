class BaseException(Exception):
    def __init__(self, message: str = "Operation error"):
        self.message = message


class InvalidTokenType(Exception):
    pass


class InvalidTokenStructure(Exception):
    pass


class UserNotFound(Exception):
    pass


class CreateObjectException(Exception):
    def __init__(self, message: str = "Server error"):
        self.message = message


class UniqueException(BaseException):
    pass


class ObjectNotFoundException(BaseException):
    pass


class ObjectUpdateException(Exception):
    pass


class AccessDeniedException(BaseException):
    pass
