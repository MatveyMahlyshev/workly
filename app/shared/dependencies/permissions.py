from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, Result
from sqlalchemy.orm import load_only

from .token import get_token_payload
from .db import get_db
from shared.infrastructure.models import User, PermissionLevel
from shared.utils.token import validate_token_type
from .token import TokenTypeFields


async def get_permission_with_token(
    payload: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(get_db),
) -> tuple:
    if not validate_token_type(
        payload=payload,
        token_type=TokenTypeFields.ACCESS_TOKEN_TYPE,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    stmt = (
        select(User)
        .options(load_only(User.permission_level))
        .where(User.uuid == payload.get("sub"))
    )
    result: Result = await session.execute(statement=stmt)
    user: User = result.scalar_one_or_none()
    return (user.permission_level, payload)


def verify_recruiter_auth(auth_data: tuple = Depends(get_permission_with_token)):
    if auth_data[0] != PermissionLevel.RECRUITER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return auth_data[1]


def verify_candidate_auth(auth_data: tuple = Depends(get_permission_with_token)):
    if auth_data[0] != PermissionLevel.CANDIDATE.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return auth_data[1]


# async def
