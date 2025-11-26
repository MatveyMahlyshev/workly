from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


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
