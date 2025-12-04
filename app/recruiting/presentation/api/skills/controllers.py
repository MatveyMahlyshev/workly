from fastapi import APIRouter, Depends, HTTPException, status

from recruiting.presentation.schemas import SkillCreate
from recruiting.application.use_cases import SkillUseCases
from shared.presentation.schemas import SuccessfullResponse
from recruiting.domain.exceptions import SkillAlreadyExists
from .dependencies import get_skill_use_cases


router = APIRouter()


@router.post("/create/", response_model=SuccessfullResponse)
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
