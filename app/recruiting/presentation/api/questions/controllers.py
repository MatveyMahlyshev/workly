from fastapi import APIRouter, Depends, HTTPException, status


from recruiting.application.use_cases import QuestionUseCases
from recruiting.presentation.schemas import Question
from shared.presentation.schemas import SuccessfullResponse
from shared.domain.exceptions import CreateObjectException
from .dependencies import get_question_use_cases

router = APIRouter()


@router.post(
    "/add/skill/{skill_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessfullResponse,
)
async def create_questions(
    skill_id: int,
    questions: list[Question],
    use_cases: QuestionUseCases = Depends(get_question_use_cases),
):
    try:
        return await use_cases.create_questions(skill_id, questions)
    except CreateObjectException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error",
        )
