from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy import select

from .schemas import PostSkill
from core.models import Skill


async def create_skill(
    skill: PostSkill,
    session: AsyncSession,
):
    new_skill = Skill(title=skill.title.lower().capitalize())

    session.add(new_skill)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Skill already exists",
        )

    return {"message": "success"}


async def get_skill_by_title(session: AsyncSession, title: str):
    title = title.lower().capitalize()
    stmt = select(Skill).where(Skill.title == title)
    skill: Skill | None = await session.scalar(statement=stmt)

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )
    return skill
