from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from api_v2.dependencies import get_db
from api_v2.schemas import SuccessResponse
from auth.dependencies import http_bearer, require_hr_or_admin
from .schemas import PostSkill, GetSkill
from . import crud

router = APIRouter()
auth = APIRouter(
    dependencies=[Depends(http_bearer), Depends(require_hr_or_admin)],
)


@router.get("/list/", response_model=list[GetSkill])
async def get_skill_list():
    pass

@auth.post(
    "/create/",
    response_model=SuccessResponse,
    responses={
        200: {"description": "Success request."},
        409: {"description": "Skill exists."},
        422: {"description": "Invalid data."},
    },
)
async def create_skill(
    skill: PostSkill,
    session: AsyncSession = Depends(get_db),
):
    return await crud.create_skill(skill=skill, session=session)


router.include_router(auth)
