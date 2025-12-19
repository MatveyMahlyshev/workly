from fastapi import APIRouter, Depends, status, HTTPException


from recruiting.presentation.schemas import (
    VacancyCreate,
    VacancyGet,
    VacancyRecruiterGet,
)
from recruiting.application.use_cases import VacancyUseCases
from .dependencies import get_vacancy_use_cases
from shared.dependencies.token import http_bearer
from shared.dependencies.permissions import verify_recruiter_auth
from shared.presentation.schemas import SuccessfullResponse
from shared.domain.exceptions import (
    CreateObjectException,
    ObjectNotFoundException,
    ObjectUpdateException,
    AccessDeniedException,
)


router = APIRouter()


@router.get(
    "/list/all/",
    response_model=list[VacancyGet],
)
async def get_vacancies(use_cases: VacancyUseCases = Depends(get_vacancy_use_cases)):
    return await use_cases.get_vacancies_list()


@router.get(
    "/my-list/",
    dependencies=[Depends(http_bearer)],
    response_model=list[VacancyRecruiterGet],
)
async def my_vacancies(
    payload: dict = Depends(verify_recruiter_auth),
    use_cases: VacancyUseCases = Depends(get_vacancy_use_cases),
):
    return await use_cases.get_vacancies_by_user(payload=payload)


@router.get(
    "/{vacancy_id}/",
    response_model=VacancyGet,
    responses={
        status.HTTP_200_OK: {"description": "Successfull request"},
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    },
)
async def get_vacancy_by_id(
    vacancy_id: int, use_cases: VacancyUseCases = Depends(get_vacancy_use_cases)
):
    try:
        return await use_cases.get_vacancy_by_id(vacancy_id=vacancy_id)
    except ObjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


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
    summary="Create vacancy draft",
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


@router.patch("/toggle/{vacancy_id}/", dependencies=[Depends(http_bearer)])
async def toggle_is_published(
    vacancy_id: int,
    use_cases: VacancyUseCases = Depends(get_vacancy_use_cases),
    payload: dict = Depends(verify_recruiter_auth),
):
    try:
        return await use_cases.toggle_is_published(payload=payload, vacancy_id=vacancy_id,)
    except AccessDeniedException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.message,
        )
    except ObjectUpdateException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error",
        )
