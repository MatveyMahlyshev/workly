from sqlalchemy import select, Select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import Tuple


from core.models import User, CandidateProfile, CandidateProfileSkillAssociation


def get_statement_for_candidate_profile(payload: dict):
    return (
        select(User)
        .options(
            selectinload(User.candidate_profile)
            .selectinload(CandidateProfile.profile_skills)
            .joinedload(CandidateProfileSkillAssociation.skill)
        )
        .where(User.email == payload.get("sub"))
    )


async def get_user_profile(
    session: AsyncSession, email: str, stmt: Select[Tuple[User]]
) -> User:
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain email",
        )
    result = await session.execute(statement=stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email or password.",
        )
    return user


def check_profile(user: User):
    if not user.candidate_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
