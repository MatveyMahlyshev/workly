from sqlite3 import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from api_v2.profiles.schemas import PutCandidateProfile

from .helpers import get_statement_for_candidate_profile
from api_v1.dependencies import get_user


async def get_profile(session: AsyncSession, payload: dict):
    email = payload.get("sub")

    user = await get_user(
        session=session,
        stmt=get_statement_for_candidate_profile(payload=payload),
        email=email,
    )

    if not user.candidate_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )

    return {
        "email": user.email,
        "name": user.candidate_profile.name,
        "surname": user.candidate_profile.surname,
        "patronymic": user.candidate_profile.patronymic,
        "about_candidate": user.candidate_profile.about_candidate,
        "education": user.candidate_profile.education,
        "birth_date": user.candidate_profile.birth_date,
        "work_experience": user.candidate_profile.work_experience,
        "skills": [
            {"title": assoc.skill.title, "id": assoc.skill.id}
            for assoc in user.candidate_profile.profile_skills
        ],
    }


async def update_profile(
    session: AsyncSession, payload: dict, data_in: PutCandidateProfile
):
    email = payload.get("sub")

    user = await get_user(
        session=session,
        stmt=get_statement_for_candidate_profile(payload=payload),
        email=email,
    )

    if not user.candidate_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )

    user.candidate_profile.name = data_in.name
    user.candidate_profile.surname = data_in.surname
    user.candidate_profile.patronymic = data_in.patronymic
    user.candidate_profile.about_candidate = data_in.about_candidate
    user.candidate_profile.education = data_in.education
    user.candidate_profile.birth_date = data_in.birth_date
    user.candidate_profile.work_experience = data_in.work_experience

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Integrity error"
        )

    return {
        "email": user.email,
        "name": user.candidate_profile.name,
        "surname": user.candidate_profile.surname,
        "patronymic": user.candidate_profile.patronymic,
        "about_candidate": user.candidate_profile.about_candidate,
        "education": user.candidate_profile.education,
        "birth_date": user.candidate_profile.birth_date,
        "work_experience": user.candidate_profile.work_experience,
        "skills": [
            {"title": assoc.skill.title, "id": assoc.skill.id}
            for assoc in user.candidate_profile.profile_skills
        ],
    }
