from fastapi import Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db import get_db
from auth.infrastructure.repositories import AuthRepositoryImpl
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
    user_repo: AuthRepositoryImpl = Depends(get_auth_repository),
):
    return AuthUseCases(repo=user_repo)
