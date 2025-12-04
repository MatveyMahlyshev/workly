from fastapi import APIRouter, Depends, HTTPException, status

from recruiting.presentation.schemas import SkillCreate, SkillGet
from recruiting.application.use_cases import SkillUseCases
from shared.presentation.schemas import SuccessfullResponse
from recruiting.domain.exceptions import SkillAlreadyExists, SkillNotFound
from .dependencies import get_skill_use_cases


router = APIRouter()


@router.post(
    "/create/",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessfullResponse,
)
async def create_skill(
    skill: SkillCreate, use_cases: SkillUseCases = Depends(get_skill_use_cases)
) -> SuccessfullResponse:
    try:
        return await use_cases.create_skill(**skill.model_dump())
    except SkillAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Skill already exists",
        )


@router.get("/list/", response_model=list[SkillGet])
async def get_skills(
    use_cases: SkillUseCases = Depends(get_skill_use_cases),
) -> SkillGet:
    return await use_cases.get_skills()


@router.get("/title/{title}/", response_model=SkillGet)
async def get_skill(
    title: str, use_cases: SkillUseCases = Depends(get_skill_use_cases)
) -> SkillGet:
    try:
        return await use_cases.get_skill(title=title)
    except SkillNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )
