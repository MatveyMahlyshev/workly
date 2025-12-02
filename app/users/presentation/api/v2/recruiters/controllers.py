from fastapi import APIRouter, Depends, status

from users.application.use_cases import RecruiterUseCase
from users.presentation.schemas import SuccessfullResponse, RecruiterCreate

from .dependencies import get_recruiter_use_cases

from ..helpers import create_user

router = APIRouter(tags=["Recruiter"], prefix="/recruiter")


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
