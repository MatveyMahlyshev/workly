from sqlalchemy.ext.asyncio import AsyncSession


from recruiting.application.interfaces import IQuestionRepository
from recruiting.domain.entities import QuestionEntity
from shared.domain.entities import SuccessfullRequestEntity


class SQLQuestionRepository(IQuestionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_questions(
        self, questions: list[QuestionEntity]
    ) -> SuccessfullRequestEntity:
        pass
