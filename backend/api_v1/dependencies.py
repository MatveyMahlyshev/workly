from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from typing import Tuple, Any
from sqlalchemy import select
from fastapi import HTTPException, status

from core.models import User
from exceptions import UnauthorizedException


async def get_user(
    session: AsyncSession, email: str, stmt: Select[Tuple[User]]
) -> User:
    if not email:
        raise UnauthorizedException.NO_EMAIL
    result = await session.execute(statement=stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email or password.",
        )
    return user


async def get_user_by_sub(
    payload: dict, session: AsyncSession, stmt: Any | None = None
):
    email = payload.get("sub")
    if stmt is None:
        stmt = select(User).where(User.email == email)
    user = await get_user(session=session, email=email, stmt=stmt)
    return user
