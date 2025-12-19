from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from recruiting.application.interfaces import ISkillRepository
from recruiting.domain.entities import SkillQuestionEntity, SkillAnswerEntity
from recruiting.infrastructure.database.models import Question, Answer
from shared.domain.entities import SuccessfullRequestEntity
from shared.domain.exceptions import (
    CreateObjectException,
    UniqueException,
    ObjectNotFoundException,
)


class SQLSkillTestRepository(ISkillRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _handle_integrity_error(
        self, e: IntegrityError, object_id: int, object_name: str = "Object"
    ) -> None:
        error_message = str(e.orig)

        if "duplicate key value violates unique constraint" in error_message:
            raise UniqueException(
                message=f"{object_name} with this text and object_id already exists"
            )

        if (
            "insert or update on table" in error_message
            or "violates foreign key constraint" in error_message
        ):
            raise ObjectNotFoundException(message=f"Object with id={object_id} not found")

        raise CreateObjectException()

    def _to_answer_model(self, question_id: int, entity: SkillAnswerEntity) -> Answer:
        return Answer(
            text=entity.text,
            is_correct=entity.is_correct,
            question_id=question_id,
        )

    def _to_question_answer_models(self, entity: SkillQuestionEntity, skill_id: int):
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
        self, skill_id: int, questions: list[SkillQuestionEntity]
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
        except IntegrityError as e:
            await self.session.rollback()
            self._handle_integrity_error(
                e=e,
                object_id=skill_id,
                object_name="Question",
            )

        return SuccessfullRequestEntity()

    async def add_answers(
        self,
        question_id: int,
        answers: list[SkillAnswerEntity],
    ) -> SuccessfullRequestEntity:
        try:
            for answer in answers:
                model = self._to_answer_model(question_id=question_id, entity=answer)
                self.session.add(model)
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            self._handle_integrity_error(
                e=e,
                object_id=question_id,
                object_name="Answer",
            )

        return SuccessfullRequestEntity()
