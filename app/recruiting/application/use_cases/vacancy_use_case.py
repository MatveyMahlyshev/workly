from ..interfaces import IVacancyRepository
from recruiting.domain.entities import VacancyEntity


class VacancyUseCases:
    def __init__(self, repo: IVacancyRepository):
        self.repo = repo

    async def create_vacancy(
        self,
        payload: dict,
        **vacancy_data: dict,
    ):
        entity = VacancyEntity(
            title=vacancy_data["title"],
            company=vacancy_data["company"],
            recruiter_id=payload.get("user_id"),
            min_salary=vacancy_data["min_salary"],
            max_salary=vacancy_data["max_salary"],
            salary_period=vacancy_data["salary_period"],
            experience=vacancy_data["experience"],
            description=vacancy_data["description"],
            skills=vacancy_data["skills"],
        )
        await self.repo.create_vacancy(entity=entity)
