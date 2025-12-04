from recruiting.application.interfaces import ISkillRepository
from recruiting.domain.entities import SkillEntity
from shared.domain.entities import SuccessfullRequestEntity


class SkillUseCases:
    def __init__(self, repo: ISkillRepository):
        self.repo = repo

    async def create_skill(self, **skill_data) -> SuccessfullRequestEntity:
        entity = SkillEntity(title=skill_data["title"])
        return await self.repo.create_skill(entity=entity)

    async def get_skill(self, title: str) -> SkillEntity:
        entity = SkillEntity(title=title)
        return await self.repo.get_skill(entity=entity)

    async def get_skills(self) -> list[SkillEntity]:
        return await self.repo.get_skills()
