from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from recruiting.application.interfaces import IQuestionRepository
from recruiting.domain.entities import QuestionEntity, AnswerEntity
from recruiting.infrastructure.database.models import Question, Answer
from shared.domain.entities import SuccessfullRequestEntity
from shared.domain.exceptions import CreateObjectException


class SQLQuestionRepository(IQuestionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_models(self, entity: QuestionEntity, skill_id: int):
        question = Question(text=entity.text, skill_id=skill_id)
        answers = [
            Answer(
                text=answer.text,
                is_correct=answer.is_correct,
                question=question,
            )
            for answer in entity.answers
        ]
        return question, answers

    async def create_questions(
        self, skill_id: int, questions: list[QuestionEntity]
    ) -> SuccessfullRequestEntity:
        for question_entity in questions:
            question, answers = self._to_models(
                entity=question_entity,
                skill_id=skill_id,
            )
            self.session.add(question)
            for answer in answers:
                self.session.add(answer)

        try:
            await self.session.commit()
        except IntegrityError:
            raise CreateObjectException()

        return SuccessfullRequestEntity()
