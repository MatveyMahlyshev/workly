from ..interfaces import IVacancyRepository
from recruiting.domain.entities import VacancyEntity


class VacancyUseCases:
    def __init__(self, repo: IVacancyRepository):
        self.repo = repo

    async def create_vacancy(self, **vacancy_data: dict):
        entity = VacancyEntity(
            title=vacancy_data["title"],
            company=vacancy_data["company"],
        )
        # self.repo.create_vacancy()
        return {"message": "Goo job"}
