from fastapi import APIRouter, Depends, status, HTTPException

from users.application.use_cases import RecruiterUseCase
from users.presentation.schemas import RecruiterCreate, RecruiterGet
from shared.presentation.schemas import SuccessfullResponse
from shared.dependencies.token import get_token_payload, http_bearer
from shared.domain.exceptions import (
    InvalidTokenType,
    InvalidTokenStructure,
    UserNotFound,
)


from .dependencies import get_recruiter_use_cases

from ..helpers import create_user

router = APIRouter()


@router.post(
    "/register/",
    response_model=SuccessfullResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Successfull request"},
        status.HTTP_409_CONFLICT: {"description": "Conflict"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Server error"},
    },
    summary="Register hr",
)
async def create_hr(
    user_data: RecruiterCreate,
    use_cases: RecruiterUseCase = Depends(get_recruiter_use_cases),
):
    return await create_user(use_cases=use_cases, user_data=user_data)


@router.post(
    "/profile/",
    response_model=RecruiterGet,
    dependencies=[Depends(http_bearer)],
    responses={
        status.HTTP_200_OK: {"description": "Successfull request"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
        status.HTTP_404_NOT_FOUND: {"description": "Not Found"},
    },
    summary="Get recruiter profile by token",
)
async def get_profile(
    payload: dict = Depends(get_token_payload),
    use_cases: RecruiterUseCase = Depends(get_recruiter_use_cases),
):
    try:
        return await use_cases.get_profile(payload=payload)
    except InvalidTokenStructure:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token structure",
        )
    except InvalidTokenType:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
