from fastapi import Depends


from infastructure.repositories.user_repo_impl import UserRepositoryImpl
from application.use_cases.user import UserUseCase
from presentation.dependencies import get_db


async def get_user_repository(session=Depends(get_db)):
    return UserRepositoryImpl(session=session)


async def get_user_use_cases(user_repo=Depends(get_user_repository)):
    return UserUseCase(repo=user_repo)
