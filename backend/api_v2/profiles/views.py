from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from api_v2.dependencies import get_db
from .schemas import GetCandidateProfileUser, PutCandidateProfile
from api_v2.skills.schemas import Skill
from auth.dependencies import get_current_token_payload, http_bearer
from . import crud
from api_v2.schemas import SuccessResponse

router = APIRouter(
    dependencies=[Depends(http_bearer)],
)


@router.get(
    "/",
    response_model=GetCandidateProfileUser,
    responses={
        200: {"description": "Success request."},
        401: {"description": "Unauthorized."},
    },
)
async def get_candidate_profile(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
):
    return await crud.get_profile(session=session, payload=payload)


@router.put(
    "/update/",
    response_model=SuccessResponse,
    responses={
        200: {"description": "Success request."},
        401: {"description": "Unauthorized."},
        422: {"description": "Invalid data."},
        500: {"description": "Integrity error."},
    },
)
async def update_profile(
    data_in: PutCandidateProfile,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
):
    return await crud.update_profile(data_in=data_in, session=session, payload=payload)


@router.put(
    "/skills/edit/",
    response_model=SuccessResponse,
    responses={
        200: {"description": "Success request."},
        401: {"description": "Unauthorized."},
        404: {"description": "Skill not found."},
        422: {"description": "Invalid data."},
        500: {"description": "Integrity error."},
    },
)
async def edit_skills_for_user(
    skills_list: list[Skill],
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
):
    return await crud.edit_user_skills(
        skills_list=skills_list,
        payload=payload,
        session=session,
    )


@router.get(
    "/skills/list/",
    response_model=list[Skill],
    responses={
        200: {"description": "Success request."},
        401: {"description": "Unauthorized."},
    },
)
async def get_user_skills(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
):
    return await crud.get_user_skills(
        payload=payload,
        session=session,
    )


@router.delete("/skills/remove/")
async def remove_skill_from_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
):
    pass
