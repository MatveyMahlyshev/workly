from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from users.infrastructure.repositories import SQLRecruiterRepositoryImpl
from users.application.use_cases import RecruiterUseCase
from users.presentation.dependencies import get_password_hasher
from dependencies.db import get_db


def get_recruiter_repository(session: AsyncSession = Depends(get_db)):
    return SQLRecruiterRepositoryImpl(session=session)


def get_recruiter_use_cases(
    user_repo=Depends(get_recruiter_repository),
    password_hasher=Depends(get_password_hasher),
):
    return RecruiterUseCase(repo=user_repo, password_hasher=password_hasher)
