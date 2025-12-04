from abc import ABC, abstractmethod


from recruiting.domain.entities import SkillEntity
from recruiting.infrastructure.database.models import Skill
from shared.domain.entities import SuccessfullRequestEntity


class ISkillRepository(ABC):

    @abstractmethod
    async def create_skill(self, entity: SkillEntity) -> SuccessfullRequestEntity:
        pass

    @abstractmethod
    async def get_skill(self, entity: SkillEntity) -> SkillEntity:
        pass

    @abstractmethod
    async def get_skills(self) -> list[SkillEntity]:
        pass

    @abstractmethod
    async def delete_skill(self, title: str) -> None:
        pass
