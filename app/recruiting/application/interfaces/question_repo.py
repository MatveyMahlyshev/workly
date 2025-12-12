from abc import ABC, abstractmethod


from recruiting.domain.entities import QuestionEntity, AnswerEntity
from shared.domain.entities import SuccessfullRequestEntity


class IQuestionRepository(ABC):

    @abstractmethod
    async def create_questions(
        self, skill_id: int, questions: list[QuestionEntity]
    ) -> SuccessfullRequestEntity:
        pass

    @abstractmethod
    async def add_answers(
        self, question_id: int, answers: list[AnswerEntity]
    ) -> SuccessfullRequestEntity:
        pass
