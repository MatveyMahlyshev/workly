from ..interfaces import IVacancyRepository, ISkillRepository
from recruiting.domain.entities import VacancyEntity, SkillEntity


class VacancyUseCases:
    def __init__(self, vacancy_repo: IVacancyRepository, skill_repo: ISkillRepository):
        self.vacancy_repo = vacancy_repo
        self.skill_repo = skill_repo

    async def create_vacancy(
        self,
        payload: dict,
        **vacancy_data: dict,
    ):
        skills = []
        titles = {skill["title"] for skill in vacancy_data["skills"]}

        if vacancy_data["skills"]:
            ids = [skill["id"] for skill in vacancy_data["skills"]]
            skills: list[SkillEntity] = list(
                filter(
                    lambda x: x.title in titles,
                    await self.skill_repo.get_skill_by_id(ids=ids),
                ),
            )

        entity = VacancyEntity(
            title=vacancy_data["title"],
            company=vacancy_data["company"],
            recruiter_id=payload.get("user_id"),
            min_salary=vacancy_data["min_salary"],
            max_salary=vacancy_data["max_salary"],
            salary_period=vacancy_data["salary_period"],
            experience=vacancy_data["experience"],
            description=vacancy_data["description"],
            skills=skills,
        )

        return await self.vacancy_repo.create_vacancy(entity=entity)

    async def get_vacancies_list(self):
        return await self.vacancy_repo.get_vacancies_list()

    async def get_vacancy_by_id(self, vacancy_id: int):
        return await self.vacancy_repo.get_vacancy_by_id(vacancy_id=vacancy_id)
