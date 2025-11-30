from fastapi import APIRouter, Depends, status, HTTPException

from application.use_cases.user import UserUseCase
from presentation.schemas import UserCreate, SuccessfullResponse
from domain.exceptions import EmailAlreadyExists
from .dependencies import get_user_use_cases

router = APIRouter(tags=["HR"], prefix="/hr")


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
    user_data: UserCreate, use_cases: UserUseCase = Depends(get_user_use_cases)
):
    try:
        await use_cases.create_user(**user_data.model_dump())
        return SuccessfullResponse()
    except EmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
