from fastapi import Form, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
import re

from core.models import User, db_helper, PermissionLevel
from .utils import validate_password
from .schemas import UserAuthSchema
from . import dependencies
import exceptions
from api_v1 import dependencies as apd
from api_v2.dependencies import get_db


def validate_email(email: str) -> str:
    """Валидация email"""
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email format. Example: user@example.com",
        )
    return email.lower()


async def validate_auth_user(
    session: AsyncSession = Depends(get_db),
    email: str = Form(...),
    password: str = Form(...),
):
    email = validate_email(email=email)

    stmt = select(User).where(User.email == email)
    result: Result = await session.execute(statement=stmt)
    user: User = result.scalar()
    if not user or not validate_password(
        password=password, hashed_password=user.password_hash
    ):
        raise exceptions.UnauthorizedException.INVALID_LOGIN_DATA

    return user


def create_access_token(user: UserAuthSchema) -> str:
    jwt_payload = {
        "sub": user.email,
        "email": user.email,
    }
    return dependencies.create_token(
        token_type=dependencies.TokenTypeFields.ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
    )


def create_refresh_token(user: UserAuthSchema) -> str:
    jwt_payload = {"sub": user.email}
    return dependencies.create_token(
        token_type=dependencies.TokenTypeFields.REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
    )


async def get_user_by_token_sub(payload: dict, session: AsyncSession):
    email: str | None = payload.get("sub")
    if not email:
        raise exceptions.UnauthorizedException.NO_EMAIL

    stmt = select(User).where(User.email == email)
    result: Result = await session.execute(statement=stmt)
    user: User = result.scalar()

    if not user:
        raise exceptions.UnauthorizedException.INVALID_LOGIN_DATA
    return user


async def get_current_auth_user_for_refresh(
    payload: dict = Depends(dependencies.get_current_token_payload),
    session: AsyncSession = Depends(get_db),
) -> UserAuthSchema:
    dependencies.validate_token_type(
        payload=payload, token_type=dependencies.TokenTypeFields.REFRESH_TOKEN_TYPE
    )
    return await get_user_by_token_sub(payload=payload, session=session)


async def check_permission(user_permission: int, permissions: list[PermissionLevel]):
    if user_permission not in permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к данному ресурсу",
        )
