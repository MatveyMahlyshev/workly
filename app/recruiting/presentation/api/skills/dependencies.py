from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from recruiting.infrastructure.respositiories import SQLSkillREpository, SQLSkillTestRepository
from recruiting.application.use_cases import SkillUseCases, SkillTestUseCases
from shared.dependencies.db import get_db


def get_skill_repo(session: AsyncSession = Depends(get_db)) -> SQLSkillREpository:
    return SQLSkillREpository(session=session)


def get_skill_use_cases(
    skill_repo: SQLSkillREpository = Depends(get_skill_repo),
) -> SkillUseCases:
    return SkillUseCases(repo=skill_repo)



def get_skill_test_repository(
    session: AsyncSession = Depends(get_db),
) -> SQLSkillTestRepository:
    return SQLSkillTestRepository(session=session)


def get_skill_tests_use_cases(
    repo: SQLSkillTestRepository = Depends(get_skill_test_repository),
) -> SkillTestUseCases:
    return SkillTestUseCases(repo=repo)
