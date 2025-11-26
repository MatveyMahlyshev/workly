from fastapi import HTTPException, status


from core.models import PermissionLevel
from .schemas import UserAuthSchema
from . import dependencies


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


async def check_permission(user_permission: int, permissions: list[PermissionLevel]):
    if user_permission not in permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
