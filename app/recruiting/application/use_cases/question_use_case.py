from recruiting.application.interfaces import IQuestionRepository
from recruiting.domain.entities import QuestionEntity, AnswerEntity
from shared.domain.entities import SuccessfullRequestEntity
from recruiting.infrastructure.database.models import Question, Answer


class QuestionUseCases:
    def __init__(self, repo: IQuestionRepository):
        self.repo = repo

    async def create_questions(
        self, skill_id: int, questions: list[Question]
    ) -> SuccessfullRequestEntity:
        question_entities: list[QuestionEntity] = []
        for question in questions:
            answers = [
                AnswerEntity(text=answer.text, is_correct=answer.is_correct)
                for answer in question.answers
            ]

            question_entities.append(
                QuestionEntity(text=question.text, answers=answers)
            )

        return await self.repo.create_questions(
            skill_id=skill_id, questions=question_entities
        )

    async def add_answers(self, question_id: int, answers: list[AnswerEntity]):
        answer_entities = [
            AnswerEntity(text=answer.text, is_correct=False) for answer in answers
        ]
        print(answer_entities)
        return await self.repo.add_answers(
            question_id=question_id,
            answers=answer_entities,
        )
