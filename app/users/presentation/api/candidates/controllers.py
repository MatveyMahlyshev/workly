from fastapi import APIRouter, Depends, status


from users.presentation.schemas import SuccessfullResponse, CandidateCreate
from users.application.use_cases import CandidateUseCase
from .dependencies import get_candidate_use_cases
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
    summary="Register candidate",
)
async def create_candidate(
    user_data: CandidateCreate,
    use_cases: CandidateUseCase = Depends(get_candidate_use_cases),
):

    return await create_user(use_cases=use_cases, user_data=user_data)
