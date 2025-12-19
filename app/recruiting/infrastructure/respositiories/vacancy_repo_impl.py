from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, Result, desc
from sqlalchemy.orm import selectinload, load_only


from recruiting.application.interfaces import IVacancyRepository
from recruiting.domain.entities import VacancyEntity, SkillEntity
from shared.infrastructure.models import Vacancy, Skill, VacancySkillAssociation
from shared.domain.entities import SuccessfullRequestEntity
from shared.domain.exceptions import (
    CreateObjectException,
    ObjectNotFoundException,
    ObjectUpdateException,
    AccessDeniedException,
)


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
            is_published=model.is_published,
            skills=[
                SkillEntity(id=assoc.skill.id, title=assoc.skill.title)
                for assoc in model.skill_associations
            ],
            created_at=model.created_at,
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
            created_at=entity.created_at,
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

    async def get_vacancy_by_id(self, vacancy_id: int):
        stmt = (
            select(Vacancy)
            .options(
                selectinload(Vacancy.skill_associations).selectinload(
                    VacancySkillAssociation.skill
                )
            )
            .where(Vacancy.id == vacancy_id)
        )
        result: Result = await self.session.execute(statement=stmt)
        vacancy: Vacancy = result.scalar_one_or_none()

        if not vacancy or not vacancy.is_published:
            raise ObjectNotFoundException(
                message=f"Vacancy with id={vacancy_id} not found"
            )

        return self._to_entity(model=vacancy)

    async def get_vacancies_by_user(self, recruiter_id: int):
        stmt = (
            select(Vacancy)
            .options(
                selectinload(Vacancy.skill_associations).selectinload(
                    VacancySkillAssociation.skill
                )
            )
            .order_by(desc(Vacancy.is_published), desc(Vacancy.created_at))
            .where(Vacancy.recruiter_id == recruiter_id)
        )

        result: Result = await self.session.execute(statement=stmt)
        vacancy_models: list[Vacancy] = result.scalars().all()
        return [self._to_entity(model=model) for model in vacancy_models]

    async def get_vacancies_list(self) -> list[VacancyEntity]:
        stmt = (
            select(Vacancy)
            .options(
                selectinload(Vacancy.skill_associations).selectinload(
                    VacancySkillAssociation.skill
                )
            )
            .order_by(desc(Vacancy.id))
        ).where(Vacancy.is_published)
        result: Result = await self.session.execute(statement=stmt)
        vacancy_models: list[Vacancy] = result.scalars().all()

        return [self._to_entity(model=model) for model in vacancy_models]

    async def delete_vacancy(self, vacancy_id):
        pass

    async def toggle_is_published(
        self, payload: dict, vacancy_id: int
    ) -> SuccessfullRequestEntity:
        stmt = (
            select(Vacancy)
            .options(load_only(Vacancy.is_published, Vacancy.recruiter_id))
            .where(Vacancy.id == vacancy_id)
        )
        result: Result = await self.session.execute(statement=stmt)
        vacancy: Vacancy = result.scalar_one_or_none()

        if not vacancy:
            raise ObjectNotFound(message="Vacancy with id={vacancy_id} not found")
        if vacancy.recruiter_id != payload.get("user_id"):
            raise AccessDeniedException(message="Access denied")

        if vacancy.is_published:
            vacancy.is_published = False
        else:
            vacancy.is_published = True

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise ObjectUpdateException()

        return SuccessfullRequestEntity()
