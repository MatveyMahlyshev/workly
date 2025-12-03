from fastapi import Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from shared.dependencies.db import get_db
from auth.infrastructure.repositories import AuthRepositoryImpl, TokenRepoImpl
from ..schemas import UserAuth
from auth.application.use_cases import AuthUseCases


def user_auth_form(
    email: str = Form(...),
    password: str = Form(...),
) -> UserAuth:
    return UserAuth(email=email, password=password)


def get_auth_repository(session: AsyncSession = Depends(get_db)):
    return AuthRepositoryImpl(session=session)


def get_auth_use_cases(
    auth_repo: AuthRepositoryImpl = Depends(get_auth_repository),
):
    return AuthUseCases(auth_repo=auth_repo, token_repo=TokenRepoImpl())
