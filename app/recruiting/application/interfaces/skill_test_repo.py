from abc import ABC, abstractmethod


from recruiting.domain.entities import SkillQuestionEntity, SkillAnswerEntity
from shared.domain.entities import SuccessfullRequestEntity


class ISkillTestRepository(ABC):

    @abstractmethod
    async def create_questions(
        self, skill_id: int, questions: list[SkillQuestionEntity]
    ) -> SuccessfullRequestEntity:
        pass

    @abstractmethod
    async def add_answers(
        self, question_id: int, answers: list[SkillAnswerEntity]
    ) -> SuccessfullRequestEntity:
        pass
