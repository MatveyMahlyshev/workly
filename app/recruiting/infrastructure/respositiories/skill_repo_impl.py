from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from recruiting.infrastructure.database.models import Skill
from recruiting.application.interfaces import ISkillRepository
from recruiting.domain.entities import SkillEntity
from recruiting.domain.exceptions import SkillAlreadyExists
from shared.domain.entities import SuccessfullRequestEntity


class SQLSkillREpository(ISkillRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_model(self, entity: SkillEntity) -> Skill:
        return Skill(title=entity.title)

    async def create_skill(self, entity: SkillEntity) -> SuccessfullRequestEntity:
        skill_model = self._to_model(entity=entity)
        try:
            self.session.add(skill_model)
            await self.session.commit()
            return SuccessfullRequestEntity()
        except IntegrityError:
            await self.session.rollback()
            raise SkillAlreadyExists()

    async def get_skill(self, title: str) -> SkillEntity:
        pass

    async def get_skills(self, title: str) -> list[SkillEntity]:
        pass

    async def delete_skill(self, title: str) -> None:
        pass
