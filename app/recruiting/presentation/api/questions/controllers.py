from fastapi import APIRouter, Depends


from recruiting.application.use_cases import QuestionUseCases
from recruiting.presentation.schemas import Question
from .dependencies import get_question_use_cases

router = APIRouter()


@router.post("/add/skill/{skill_id}")
async def create_questions(
    skill_id: int,
    questions: list[Question],
    use_cases: QuestionUseCases = Depends(get_question_use_cases),
):
    return await use_cases.create_questions(skill_id, questions)
