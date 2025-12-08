from sqlalchemy.ext.asyncio import AsyncSession


from recruiting.application.interfaces import IVacancyRepository


class SQLVacancyRepository(IVacancyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_vacancy(self, entity):
        pass

    async def get_vacancy(self, vacancy_id):
        pass

    async def delete_vacancy(self, vacancy_id):
        pass
