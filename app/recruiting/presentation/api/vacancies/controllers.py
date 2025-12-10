from fastapi import APIRouter, Depends, status, HTTPException


from recruiting.presentation.schemas import VacancyCreate
from recruiting.application.use_cases import VacancyUseCases
from .dependencies import get_vacancy_use_cases
from shared.dependencies.token import http_bearer, get_token_payload
from shared.dependencies.permissions import verify_recruiter_auth
from shared.presentation.schemas import SuccessfullResponse
from shared.domain.exceptions import CreateObjectException


router = APIRouter()


@router.post(
    "/create/vacancy/",
    dependencies=[Depends(http_bearer)],
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessfullResponse,
    responses={
        status.HTTP_201_CREATED: {"description": "Successfull request"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Server error"},
    },
)
async def create_vacancy(
    vacancy_data: VacancyCreate,
    use_cases: VacancyUseCases = Depends(get_vacancy_use_cases),
    payload: dict = Depends(verify_recruiter_auth),
):
    try:
        return await use_cases.create_vacancy(
            payload=payload, **vacancy_data.model_dump()
        )
    except CreateObjectException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error",
        )
