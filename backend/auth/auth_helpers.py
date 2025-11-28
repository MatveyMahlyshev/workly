from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from functools import wraps

from core.models import PermissionLevel
from .schemas import UserAuthSchema
from . import dependencies
from api_v2.dependencies import get_db


def create_access_token(user: UserAuthSchema) -> str:
    jwt_payload = {"sub": user.email}
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
