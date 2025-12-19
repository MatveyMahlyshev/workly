from fastapi import APIRouter, Depends, HTTPException, status

from recruiting.presentation.schemas import SkillCreate, SkillGet, Question, Answer
from recruiting.application.use_cases import SkillUseCases
from shared.presentation.schemas import SuccessfullResponse
from recruiting.domain.exceptions import SkillAlreadyExists
from recruiting.application.use_cases import SkillTestUseCases
from shared.domain.exceptions import (
    CreateObjectException,
    UniqueException,
    ObjectNotFoundException,
)
from .dependencies import get_skill_use_cases, get_skill_tests_use_cases


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


@router.post(
    "/{skill_id}/add/question/",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessfullResponse,
    responses={
        status.HTTP_201_CREATED: {"description": "Successfull request"},
        status.HTTP_404_NOT_FOUND: {"description": "Not Found"},
        status.HTTP_409_CONFLICT: {"description": "Conflict"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Server error"},
    },
)
async def create_questions(
    skill_id: int,
    questions: list[Question],
    use_cases: SkillTestUseCases = Depends(get_skill_tests_use_cases),
):
    try:
        return await use_cases.create_questions(skill_id=skill_id, questions=questions)
    except UniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except ObjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except CreateObjectException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )


@router.post(
    "/{question_id}/add/answers/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Successfull request"},
        status.HTTP_404_NOT_FOUND: {"description": "Not Found"},
        status.HTTP_409_CONFLICT: {"description": "Conflict"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Server error"},
    },
    response_model=SuccessfullResponse,
)
async def add_answers(
    qustion_id: int,
    answers: list[Answer],
    use_cases: SkillTestUseCases = Depends(get_skill_tests_use_cases),
):
    try:
        return await use_cases.add_answers(question_id=qustion_id, answers=answers)
    except UniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except ObjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except CreateObjectException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )
