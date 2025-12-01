from fastapi import Depends

from infastructure.database.session import db_helper
from infastructure.utils.password_hasher import BcryptPasswordHasher


async def get_db():
    async with db_helper.session_dependency() as session:
        yield session


def get_password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher()
