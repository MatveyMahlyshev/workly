from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from recruiting.infrastructure.respositiories import SQLVacancyRepository
from recruiting.application.use_cases import VacancyUseCases
from shared.dependencies.db import get_db


def get_vacancy_repo(session: AsyncSession = Depends(get_db)):
    return SQLVacancyRepository(session=session)


def get_vacancy_use_cases(repo: SQLVacancyRepository = Depends(get_vacancy_repo)):
    return VacancyUseCases(repo=SQLVacancyRepository)
