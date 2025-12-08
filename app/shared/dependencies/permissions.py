from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, Result
from sqlalchemy.orm import load_only

from .token import get_token_payload
from .db import get_db
from shared.infrastructure.users.models import User, PermissionLevel


async def get_permission(
    payload: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(get_db),
) -> int:

    stmt = (
        select(User)
        .options(load_only(User.permission_level))
        .where(User.email == payload.get("sub"))
    )
    result: Result = await session.execute(statement=stmt)
    user: User = result.scalar_one_or_none()
    return user.permission_level


async def only_recruiter_permission(user_permission: int = Depends(get_permission)):
    if user_permission != PermissionLevel.RECRUITER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )


async def only_candidate_permission(user_permission: int = Depends(get_permission)):
    if user_permission != PermissionLevel.CANDIDATE.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )


# async def
