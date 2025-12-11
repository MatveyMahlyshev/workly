from abc import ABC, abstractmethod


from recruiting.domain.entities import QuestionEntity
from shared.domain.entities import SuccessfullRequestEntity


class IQuestionRepository(ABC):

    @abstractmethod
    async def create_questions(
        self, skill_id, questions: list[QuestionEntity]
    ) -> SuccessfullRequestEntity:
        pass
