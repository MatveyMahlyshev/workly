from fastapi import APIRouter, Depends


from recruiting.presentation.schemas import VacancyCreate
from recruiting.application.use_cases import VacancyUseCases
from .dependencies import get_vacancy_use_cases
from shared.dependencies.token import http_bearer
from shared.dependencies.permissions import only_recruiter_permission

router = APIRouter()


@router.post("/create/vacancy/", dependencies=[Depends(http_bearer), Depends(only_recruiter_permission)])
async def create_vacancy(
    vacancy_data: VacancyCreate,
    use_cases: VacancyUseCases = Depends(get_vacancy_use_cases),
):
    return await use_cases.create_vacancy(**vacancy_data.model_dump())
