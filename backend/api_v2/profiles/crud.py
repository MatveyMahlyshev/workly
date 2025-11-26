from sqlite3 import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select

from .schemas import PutCandidateProfile, GetCandidateProfileUser
from api_v2.skills.schemas import Skill
from api_v2.schemas import SuccessResponse

from core.models import CandidateProfileSkillAssociation, Skill as skill_model

from .helpers import (
    get_statement_for_candidate_profile,
    get_user_profile,
    check_profile,
)


async def get_profile(session: AsyncSession, payload: dict):
    user = await get_user_profile(
        session=session,
        stmt=get_statement_for_candidate_profile(payload=payload),
        email=payload.get("sub"),
    )

    check_profile(user=user)

    return GetCandidateProfileUser(
        email=user.email,
        name=user.candidate_profile.name,
        surname=user.candidate_profile.surname,
        patronymic=user.candidate_profile.patronymic,
        about_candidate=user.candidate_profile.about_candidate,
        education=user.candidate_profile.education,
        birth_date=user.candidate_profile.birth_date,
        work_experience=user.candidate_profile.work_experience,
        skills=[
            {"title": assoc.skill.title, "id": assoc.skill.id}
            for assoc in user.candidate_profile.profile_skills
        ],
    )


async def update_profile(
    session: AsyncSession, payload: dict, data_in: PutCandidateProfile
):
    user = await get_user_profile(
        session=session,
        stmt=get_statement_for_candidate_profile(payload=payload),
        email=payload.get("sub"),
    )

    check_profile(user=user)

    profile = user.candidate_profile

    for field, value in data_in.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Integrity error")

    return SuccessResponse(message="success")


async def edit_user_skills(
    skills_list: list[Skill],
    session: AsyncSession,
    payload: dict,
):
    user = await get_user_profile(
        session=session,
        stmt=get_statement_for_candidate_profile(payload=payload),
        email=payload.get("sub"),
    )
    check_profile(user=user)

    skill_titles = [skill.title.lower().capitalize() for skill in skills_list]
    stmt = select(skill_model).where(skill_model.title.in_(skill_titles))
    result = await session.execute(statement=stmt)
    existing_skills = result.scalars().all()

    found_titles = {skill.title for skill in existing_skills}
    missing_skills = set(skill_titles) - found_titles
    if missing_skills:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skills not found: {', '.join(missing_skills)}",
        )

    profile_id = user.candidate_profile.id
    skill_ids = [skill.id for skill in existing_skills]
    stmt = select(CandidateProfileSkillAssociation).where(
        CandidateProfileSkillAssociation.candidate_profile_id == profile_id,
        CandidateProfileSkillAssociation.skill_id.in_(skill_ids),
    )
    result = await session.execute(stmt)
    existing_associations = result.scalars().all()

    existing_skill_ids = {assoc.skill_id for assoc in existing_associations}
    for skill in existing_skills:
        if skill.id not in existing_skill_ids:
            association = CandidateProfileSkillAssociation(
                candidate_profile_id=user.candidate_profile.id,
                skill_id=skill.id,
            )
            session.add(association)

    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Integrity error",
        )
    return SuccessResponse(message="success")


async def get_user_skills(
    session: AsyncSession,
    payload: dict,
):

    user = await get_user_profile(
        session=session,
        stmt=get_statement_for_candidate_profile(payload=payload),
        email=payload.get("sub"),
    )

    return [skill.skill for skill in user.candidate_profile.profile_skills]
