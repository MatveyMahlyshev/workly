from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from recruiting.application.interfaces import IQuestionRepository
from recruiting.domain.entities import QuestionEntity, AnswerEntity
from recruiting.infrastructure.database.models import Question, Answer
from shared.domain.entities import SuccessfullRequestEntity
from shared.domain.exceptions import CreateObjectException, UniqueException


class SQLQuestionRepository(IQuestionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_answer_model(self, question_id: int, entity: AnswerEntity) -> Answer:
        return Answer(
            text=entity.text,
            is_correct=entity.is_correct,
            question_id=question_id,
        )

    def _to_question_answer_models(self, entity: QuestionEntity, skill_id: int):
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
            question, answers = self._to_question_answer_models(
                entity=question_entity,
                skill_id=skill_id,
            )
            self.session.add(question)
            for answer in answers:
                self.session.add(answer)

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise CreateObjectException()

        return SuccessfullRequestEntity()

    async def add_answers(
        self,
        question_id: int,
        answers: list[AnswerEntity],
    ) -> SuccessfullRequestEntity:
        try:
            for answer in answers:
                model = self._to_answer_model(question_id=question_id, entity=answer)
                self.session.add(model)
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            if "duplicate key value violates unique constraint" in str(e._message):
                raise UniqueException(message="Answer with this text already exists")
            else:
                raise CreateObjectException(message="Server error")

        return SuccessfullRequestEntity()
