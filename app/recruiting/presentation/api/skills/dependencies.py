from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from recruiting.infrastructure.respositiories import SQLSkillREpository
from recruiting.application.use_cases import SkillUseCases
from shared.dependencies.db import get_db


def get_skill_repo(session: AsyncSession = Depends(get_db)) -> SQLSkillREpository:
    return SQLSkillREpository(session=session)


def get_skill_use_cases(
    skill_repo: SQLSkillREpository = Depends(get_skill_repo),
) -> SkillUseCases:
    return SkillUseCases(repo=skill_repo)
