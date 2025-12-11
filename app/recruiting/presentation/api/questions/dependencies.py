from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from recruiting.infrastructure.respositiories import SQLQuestionRepository
from recruiting.application.use_cases import QuestionUseCases
from shared.dependencies.db import get_db


def get_question_repository(
    session: AsyncSession = Depends(get_db),
) -> SQLQuestionRepository:
    return SQLQuestionRepository(session=session)


def get_question_use_cases(
    repo: SQLQuestionRepository = Depends(get_question_repository),
) -> QuestionUseCases:
    return QuestionUseCases(repo=repo)
