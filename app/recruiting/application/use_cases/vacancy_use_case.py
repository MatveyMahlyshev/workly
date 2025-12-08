from ..interfaces import IVacancyRepository

class VacancyUseCases:
    def __init__(self, repo: IVacancyRepository):
        self.repo = repo

    async def create_vacancy(self, ):
        pass