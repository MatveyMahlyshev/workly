from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, Result, desc
from sqlalchemy.orm import selectinload


from recruiting.application.interfaces import IVacancyRepository
from recruiting.domain.entities import VacancyEntity, SkillEntity
from shared.infrastructure.models import Vacancy, Skill, VacancySkillAssociation
from shared.domain.entities import SuccessfullRequestEntity
from shared.domain.exceptions import CreateObjectException


class SQLVacancyRepository(IVacancyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: Vacancy) -> VacancyEntity:
        return VacancyEntity(
            id=model.id,
            title=model.title,
            company=model.company,
            min_salary=model.min_salary,
            max_salary=model.max_salary,
            salary_period=model.salary_period,
            experience=model.experience,
            description=model.description,
            recruiter_id=model.recruiter_id,
            skills=[
                SkillEntity(id=assoc.skill.id, title=assoc.skill.title)
                for assoc in model.skill_associations
            ],
        )

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
            await self.session.commit()
        except IntegrityError:
            raise CreateObjectException()

        return SuccessfullRequestEntity()

    async def get_vacancy(self, vacancy_id):
        pass

    async def get_vacancies_list(self) -> list[VacancyEntity]:
        stmt = (
            select(Vacancy)
            .options(
                selectinload(Vacancy.skill_associations).selectinload(
                    VacancySkillAssociation.skill
                )
            )
            .order_by(desc(Vacancy.id))
        )
        result: Result = await self.session.execute(statement=stmt)
        vacancy_models: list[Vacancy] = result.scalars().all()
   
        return [self._to_entity(model=model) for model in vacancy_models]

    async def delete_vacancy(self, vacancy_id):
        pass
