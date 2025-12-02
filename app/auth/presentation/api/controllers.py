from fastapi import APIRouter, Depends, HTTPException, status

from ..schemas import UserAuth, Token
from .dependencies import user_auth_form, get_auth_use_cases
from auth.application.use_cases import AuthUseCases
from auth.domain.exceptions import InvalidLoginData, UserNotFound, AuthError

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={
        status.HTTP_200_OK: {"description": "Successfull request"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Login error"},
    },
    summary="Login user",
)
async def login(
    login_data: UserAuth = Depends(user_auth_form),
    use_cases: AuthUseCases = Depends(get_auth_use_cases),
):
    try:
        return await use_cases.login(login_data=login_data)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except InvalidLoginData:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid login data",
        )
    except AuthError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login error",
        )
