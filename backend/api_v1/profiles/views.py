from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CandidateProfileUser, CandidateProfileUpdate
from auth.dependencies import get_current_token_payload, http_bearer
from . import crud
from core.models import db_helper
from api_v2.dependencies import get_db

from api_v1.skills.schemas import SkillBase


router = APIRouter(
    dependencies=[Depends(http_bearer)],
)


@router.get("/candidate/me/")
async def get_candidate_profile(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
) -> CandidateProfileUser:
    return await crud.get_user_with_profile_by_token(session=session, payload=payload)


@router.put("/candidate/me/edit/")
async def update_candidate_profile(
    data_to_update: CandidateProfileUpdate,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
) -> CandidateProfileUpdate:
    return await crud.update_candidate_profile(
        profile_data=data_to_update, session=session, payload=payload
    )


@router.put("/candidate/me/edit/skills/")
async def update_candidate_profile_skills(
    skills_in: list[SkillBase],
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
) -> list[SkillBase]:
    return await crud.update_candidate_profile_skills(
        skills=skills_in, payload=payload, session=session
    )


@router.get("/candidate/me/tests/")
async def get_candidate_tests(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
):
    return await crud.get_candidate_tests(payload=payload, session=session)
