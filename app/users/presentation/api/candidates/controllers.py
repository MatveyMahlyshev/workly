from fastapi import APIRouter, Depends, status, HTTPException



from users.presentation.schemas import CandidateCreate
from users.application.use_cases import CandidateUseCase
from shared.presentation.schemas import SuccessfullResponse
from .dependencies import get_candidate_use_cases
from ..helpers import create_user
from shared.dependencies.token import get_current_token_payload, http_bearer
from shared.domain.exceptions import InvalidTokenType


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


@router.get("/profile/", dependencies=[Depends(http_bearer)])
async def get_candidate_profile(
    payload: dict = Depends(get_current_token_payload),
    use_cases: CandidateUseCase = Depends(get_candidate_use_cases),
):
    try:
        return await use_cases.get_profile(payload=payload)
    except InvalidTokenType:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )