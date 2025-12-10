from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from recruiting.application.interfaces import IVacancyRepository
from recruiting.domain.entities import VacancyEntity
from shared.infrastructure.models import Vacancy
from shared.domain.entities import SuccessfullRequestEntity
from shared.domain.exceptions import CreateObjectException


class SQLVacancyRepository(IVacancyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_model(self, entity: VacancyEntity) -> Vacancy:
        return Vacancy(
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

    async def create_vacancy(self, entity: VacancyEntity):
        model = self._to_model(entity=entity)
        self.session.add(model)

        try:
            await self.session.commit()
        except IntegrityError:
            raise CreateObjectException()

        return SuccessfullRequestEntity()

    async def get_vacancy(self, vacancy_id):
        pass

    async def delete_vacancy(self, vacancy_id):
        pass
