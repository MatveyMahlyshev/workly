from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

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
