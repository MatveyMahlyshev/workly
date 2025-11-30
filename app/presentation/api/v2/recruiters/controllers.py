from fastapi import APIRouter, Depends, status, HTTPException

from application.use_cases import RecruiterUseCase
from presentation.schemas import SuccessfullResponse, RecruiterCreate
from domain.exceptions import EmailAlreadyExists, PhoneAlreadyExists
from .dependencies import get_recruiter_use_cases

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
    try:
        await use_cases.create_user(**user_data.model_dump())
        return SuccessfullResponse()
    except EmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    except PhoneAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already registered",
        )
