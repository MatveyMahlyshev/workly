from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result


from recruiting.application.interfaces import IVacancyRepository
from recruiting.domain.entities import VacancyEntity
from shared.infrastructure.models import User, Recruiter


class SQLVacancyRepository(IVacancyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_vacancy(self, payload: dict, entity: VacancyEntity):
        stmt = select(Recruiter).where(Recruiter.user.email == payload.get("sub"))
        result: Result = await self.session.execute(statement=stmt)

    async def get_vacancy(self, vacancy_id):
        pass

    async def delete_vacancy(self, vacancy_id):
        pass
