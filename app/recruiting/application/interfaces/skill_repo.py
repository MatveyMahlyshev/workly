from abc import ABC, abstractmethod


from recruiting.domain.entities import SkillEntity


class ISkillRepository(ABC):

    @abstractmethod
    async def create_skill(self, title: str) -> SkillEntity:
        pass

    @abstractmethod
    async def get_skill(self, title: str) -> SkillEntity:
        pass

    @abstractmethod
    async def get_skills(self, title: str) -> SkillEntity:
        pass

    @abstractmethod
    async def delete_skill(self, title: str) -> None:
        pass
