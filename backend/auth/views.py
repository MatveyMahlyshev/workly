from fastapi import APIRouter, Depends


from .auth_helpers import (
    create_access_token,
    create_refresh_token,
)
from .schemas import TokenInfo, UserAuthSchema
from core.models import User
from .dependencies import (
    http_bearer,
    validate_auth_user,
    get_current_auth_user_for_refresh,
)


router = APIRouter()
auth = APIRouter(dependencies=[Depends(http_bearer)])


@router.post(
    "/login/",
    response_model=TokenInfo,
    responses={
        200: {"description": "Success request."},
        404: {"description": "User doesn't exist."},
        422: {"description": "Invalid login data."},
        500: {"description": "Internal server error."},
    },
)
async def login_user(user: UserAuthSchema = Depends(validate_auth_user)):

    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@auth.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
    responses={
        200: {"description": "Success request."},
        401: {"description": "Unauthorized."},
    },
)
async def auth_refresh(
    user: UserAuthSchema = Depends(get_current_auth_user_for_refresh),
):
    access_token = create_access_token(user=user)
    return TokenInfo(access_token=access_token)


router.include_router(router=auth)
