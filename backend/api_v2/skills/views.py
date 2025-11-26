from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from api_v2.dependencies import get_db
from api_v2.schemas import SuccessResponse
from .schemas import PostSkill
from . import crud

router = APIRouter()


@router.post("/create/", response_model=SuccessResponse, responses={
    200: {"description": "Success request."},
    409: {"description": "Skill exists."},
    422: {"description": "Invalid data."},
})
async def create_skill(
    skill: PostSkill,
    session: AsyncSession = Depends(get_db),
):
    return await crud.create_skill(skill=skill, session=session)
