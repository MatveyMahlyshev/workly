from fastapi import APIRouter, Depends, HTTPException, status


from recruiting.application.use_cases import QuestionUseCases
from recruiting.presentation.schemas import Question, Answer
from shared.presentation.schemas import SuccessfullResponse
from shared.domain.exceptions import CreateObjectException, UniqueException
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
        return await use_cases.create_questions(skill_id=skill_id, questions=questions)
    except CreateObjectException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error",
        )


@router.post("/{question_id}/add/answers/")
async def create_answers(
    qustion_id: int,
    answers: list[Answer],
    use_cases: QuestionUseCases = Depends(get_question_use_cases),
):
    try:
        return await use_cases.add_answers(question_id=qustion_id, answers=answers)
    except UniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except CreateObjectException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )
