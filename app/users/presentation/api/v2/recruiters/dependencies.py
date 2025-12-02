from fastapi import Depends


from users.infrastructure.repositories import RecruiterRepositoryImpl
from users.application.use_cases import RecruiterUseCase
from users.presentation.dependencies import  get_password_hasher
from dependencies.db import get_db


def get_recruiter_repository(session=Depends(get_db)):
    return RecruiterRepositoryImpl(session=session)


def get_recruiter_use_cases(
    user_repo=Depends(get_recruiter_repository),
    password_hasher=Depends(get_password_hasher),
):
    return RecruiterUseCase(repo=user_repo, password_hasher=password_hasher)
