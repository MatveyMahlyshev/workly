from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from recruiting.application.interfaces import IVacancyRepository
from recruiting.domain.entities import VacancyEntity, SkillEntity
from shared.infrastructure.models import Vacancy, Skill, VacancySkillAssociation
from shared.domain.entities import SuccessfullRequestEntity
from shared.domain.exceptions import CreateObjectException


class SQLVacancyRepository(IVacancyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def vacancy_skill_association(
        self, skill_entities: list[SkillEntity]
    ) -> list[Skill]:

        for entity in skill_entities:
            entity.title

    def _to_model(self, entity: VacancyEntity) -> Vacancy:
        vacancy = Vacancy(
            title=entity.title,
            min_salary=entity.min_salary,
            max_salary=entity.max_salary,
            salary_period=entity.salary_period,
            experience=entity.experience,
            description=entity.description,
            company=entity.company,
            is_published=entity.is_published,
            recruiter_id=entity.recruiter_id,
        )
        vacancy_skills = [
            VacancySkillAssociation(skill_id=skill.id, vacancy=vacancy)
            for skill in entity.skills
        ]
        return vacancy, vacancy_skills

    async def create_vacancy(self, entity: VacancyEntity):
        try:
            vacancy_model, vacancy_skills_models = self._to_model(entity=entity)
            self.session.add(vacancy_model)
            for vacancy_skills_model in vacancy_skills_models:
                self.session.add(vacancy_skills_model)
            # await self.session.commit()
        except IntegrityError:
            raise CreateObjectException()

        return SuccessfullRequestEntity()

    async def get_vacancy(self, vacancy_id):
        pass

    async def delete_vacancy(self, vacancy_id):
        pass
