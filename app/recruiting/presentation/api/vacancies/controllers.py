from fastapi import APIRouter, Depends


from recruiting.presentation.schemas import VacancyCreate
from recruiting.application.use_cases import VacancyUseCases
from .dependencies import get_vacancy_use_cases
from shared.dependencies.token import http_bearer, get_token_payload
from shared.dependencies.permissions import verify_recruiter_auth


router = APIRouter()


@router.post(
    "/create/vacancy/",
    dependencies=[Depends(http_bearer)],
)
async def create_vacancy(
    vacancy_data: VacancyCreate,
    use_cases: VacancyUseCases = Depends(get_vacancy_use_cases),
    payload: dict = Depends(verify_recruiter_auth),
):
    return await use_cases.create_vacancy(payload=payload, **vacancy_data.model_dump())
