from recruiting.application.interfaces import ISkillRepository
from recruiting.domain.entities import SkillEntity
from shared.domain.entities import SuccessfullRequestEntity


class SkillUseCases:
    def __init__(self, repo: ISkillRepository):
        self.repo = repo

    async def create_skill(self, **skill_data) -> SuccessfullRequestEntity:
        entity = SkillEntity(title=skill_data["title"])
        return await self.repo.create_skill(entity=entity)
