from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import SkillTestCreate, SkillTest, SkillTestAnswers
from core.models import db_helper
from api_v1.skill_tests import crud
from auth.dependencies import get_current_token_payload
from api_v2.dependencies import get_db

router = APIRouter()


@router.post("/create/", response_model=SkillTest)
async def create_question_with_answers(
    question: SkillTestCreate,
    session: AsyncSession = Depends(get_db),
):
    return await crud.create_skill_question(question=question, session=session)


@router.get("/test/{skill_id}/{response_id}/", response_model=list[SkillTest])
async def get_test_by_skill(
    response_id: int,
    skill_id: int,
    session: AsyncSession = Depends(get_db),
):
    return await crud.get_test_by_skill(skill_id=skill_id, session=session)


@router.post("/test/accept/")
async def accept_test(
    answers: list[SkillTestAnswers],
    session: AsyncSession = Depends(get_db),
    payload: dict = Depends(get_current_token_payload),
):
    return await crud.accept_test(
        answers=answers,
        session=session,
        payload=payload,
    )
