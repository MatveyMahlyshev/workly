from fastapi import Depends

from infastructure.database.session import db_helper
from infastructure.repositories.user_repo_impl import UserRepositoryImpl
from application.use_cases.user import UserUseCase


async def get_db():
    async with db_helper.session_dependency() as session:
        yield session


async def get_user_repository(session=Depends(get_db)):
    return UserRepositoryImpl(session=session)


async def get_user_use_cases(user_repo=Depends(get_user_repository)):
    return UserUseCase(repo=user_repo)
