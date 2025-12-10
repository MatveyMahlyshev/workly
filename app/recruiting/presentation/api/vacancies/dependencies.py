from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from recruiting.infrastructure.respositiories import SQLVacancyRepository
from recruiting.application.use_cases import VacancyUseCases
from shared.dependencies.db import get_db
from ..skills.dependencies import get_skill_repo, SQLSkillREpository


def get_vacancy_repo(session: AsyncSession = Depends(get_db)):
    return SQLVacancyRepository(session=session)


def get_vacancy_use_cases(
    vacancy_repo: SQLVacancyRepository = Depends(get_vacancy_repo),
    skill_repo: SQLSkillREpository = Depends(get_skill_repo),
):
    return VacancyUseCases(vacancy_repo=vacancy_repo, skill_repo=skill_repo)
