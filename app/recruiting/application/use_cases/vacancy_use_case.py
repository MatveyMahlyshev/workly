from ..interfaces import IVacancyRepository, ISkillRepository
from recruiting.domain.entities import (
    VacancyEntity,
    SkillEntity,
    VacancyInitialQuestionTextEntity,
)
from shared.domain.entities import SuccessfullRequestEntity


class VacancyUseCases:
    def __init__(self, vacancy_repo: IVacancyRepository, skill_repo: ISkillRepository):
        self.vacancy_repo = vacancy_repo
        self.skill_repo = skill_repo

    async def create_vacancy(
        self,
        payload: dict,
        **vacancy_data: dict,
    ) -> SuccessfullRequestEntity:
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

    async def get_vacancies_by_user(self, payload: dict) -> list[VacancyEntity]:
        return await self.vacancy_repo.get_vacancies_by_user(
            recruiter_id=payload.get("user_id")
        )

    async def get_vacancies_list(self) -> list[VacancyEntity]:
        return await self.vacancy_repo.get_vacancies_list()

    async def get_vacancy_by_id(self, vacancy_id: int) -> VacancyEntity:
        return await self.vacancy_repo.get_vacancy_by_id(vacancy_id=vacancy_id)

    async def toggle_is_published(
        self, payload: dict, vacancy_id: int
    ) -> SuccessfullRequestEntity:
        return await self.vacancy_repo.toggle_is_published(
            payload=payload,
            vacancy_id=vacancy_id,
        )

    async def create_initial_questions(
        self,
        payload: dict,
        vacancy_id: int,
        questions: list[VacancyInitialQuestionTextEntity],
    ) -> SuccessfullRequestEntity:
        return await self.vacancy_repo.create_initial_questions(
            payload=payload,
            vacancy_id=vacancy_id,
            questions=questions,
        )
