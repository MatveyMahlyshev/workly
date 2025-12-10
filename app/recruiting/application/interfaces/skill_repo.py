from abc import ABC, abstractmethod


from recruiting.domain.entities import SkillEntity
from shared.domain.entities import SuccessfullRequestEntity


class ISkillRepository(ABC):

    @abstractmethod
    async def create_skill(self, entity: SkillEntity) -> SuccessfullRequestEntity:
        pass

    @abstractmethod
    async def get_skill_by_title(self, entity: SkillEntity) -> SkillEntity | None:
        pass

    @abstractmethod
    async def get_skill_by_id(self, ids: list[int]) -> SkillEntity | None:
        pass

    @abstractmethod
    async def get_skills(self) -> list[SkillEntity]:
        pass

    @abstractmethod
    async def delete_skill(self, title: str) -> None:
        pass
