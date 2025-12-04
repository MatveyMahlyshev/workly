from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, Result, asc

from recruiting.infrastructure.database.models import Skill
from recruiting.application.interfaces import ISkillRepository
from recruiting.domain.entities import SkillEntity
from recruiting.domain.exceptions import SkillAlreadyExists, SkillNotFound
from shared.domain.entities import SuccessfullRequestEntity


class SQLSkillREpository(ISkillRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_model(self, entity: SkillEntity) -> Skill:
        return Skill(title=entity.title)

    def _to_entity(self, model: Skill) -> SkillEntity:
        return SkillEntity(title=model.title)

    async def create_skill(self, entity: SkillEntity) -> SuccessfullRequestEntity:
        skill_model: Skill = self._to_model(entity=entity)
        try:
            self.session.add(skill_model)
            await self.session.commit()
            return SuccessfullRequestEntity()
        except IntegrityError:
            await self.session.rollback()
            raise SkillAlreadyExists()

    async def get_skill(self, entity: SkillEntity) -> SkillEntity:
        stmt = select(Skill).where(Skill.title == entity.title)
        result: Result = await self.session.execute(statement=stmt)
        skill = result.scalar_one_or_none()
        if not skill:
            raise SkillNotFound()
        return self._to_entity(model=skill)

    async def get_skills(self) -> list[SkillEntity]:
        stmt = select(Skill).order_by(asc(Skill.id))
        result: Result = await self.session.execute(statement=stmt)
        skills_models: list[Skill] = list(result.scalars().all())
        skills = [self._to_entity(model=skill_model) for skill_model in skills_models]
        return skills

    async def delete_skill(self, title: str) -> None:
        pass
