from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from api_v2.dependencies import get_db
from .schemas import GetCandidateProfileUser, PutCandidateProfile
from auth.dependencies import get_current_token_payload, http_bearer
from . import crud

router = APIRouter(
    dependencies=[Depends(http_bearer)],
)


@router.get("/", response_model=GetCandidateProfileUser)
async def get_candidate_profile(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
):
    return await crud.get_profile(session=session, payload=payload)


@router.put("/edit/")
async def update_profile(
    data_in: PutCandidateProfile,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
):
    return await crud.update_profile(data_in=data_in, session=session, payload=payload)
