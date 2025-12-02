from fastapi import Depends

from users.infrastructure.utils.password_hasher import BcryptPasswordHasher


def get_password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher()
