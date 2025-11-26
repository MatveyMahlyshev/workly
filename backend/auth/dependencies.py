from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi import Depends, HTTPException, status, Form
from jwt.exceptions import InvalidTokenError
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select


from .utils import encode_jwt, decode_jwt
from core.config import settings
from core.models import User
from .schemas import UserAuthSchema
from api_v2.dependencies import get_db
from .utils import validate_password


class TokenTypeFields:
    TOKEN_TYPE_FIELD = "type"
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/auth/login/")
http_bearer = HTTPBearer(auto_error=False)


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token.",
        )
    return payload


def create_token(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    jwt_payload = {TokenTypeFields.TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def validate_token_type(payload: dict, token_type: str) -> bool:
    if payload.get(TokenTypeFields.TOKEN_TYPE_FIELD) == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Error type of token.",
    )


def user_auth_form(
    email: str = Form(...),
    password: str = Form(...),
) -> UserAuthSchema:
    return UserAuthSchema(email=email, password=password)


async def validate_auth_user(
    session: AsyncSession = Depends(get_db),
    user_data: UserAuthSchema = Depends(user_auth_form),
):

    stmt = select(User).where(User.email == user_data.email)
    result: Result = await session.execute(statement=stmt)
    user: User = result.scalar()
    if not user or not validate_password(
        password=user_data.password, hashed_password=user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email or password.",
        )
    return user


async def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
) -> UserAuthSchema:
    validate_token_type(
        payload=payload,
        token_type=TokenTypeFields.REFRESH_TOKEN_TYPE,
    )
    return await get_user_by_token_sub(payload=payload, session=session)


async def get_user_by_token_sub(payload: dict, session: AsyncSession):
    email: str | None = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email or password.",
        )

    stmt = select(User).where(User.email == email)
    result: Result = await session.execute(statement=stmt)
    user: User = result.scalar()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email or password.",
        )
    return user
