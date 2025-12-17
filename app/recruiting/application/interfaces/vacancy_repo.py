from abc import ABC, abstractmethod


from recruiting.domain.entities import VacancyEntity
from shared.domain.entities import SuccessfullRequestEntity


class IVacancyRepository(ABC):

    @abstractmethod
    async def create_vacancy(self, entity: VacancyEntity) -> SuccessfullRequestEntity:
        pass

    @abstractmethod
    async def get_vacancy_by_id(self, vacancy_id: int) -> VacancyEntity:
        pass

    @abstractmethod
    async def get_vacancies_by_user(self, recruiter_id: int) -> list[VacancyEntity]:
        pass

    @abstractmethod
    async def get_vacancies_list(self) -> list[VacancyEntity]:
        pass

    @abstractmethod
    async def delete_vacancy(self, vacancy_id: int) -> None:
        pass

    async def toggle_is_published(self, vacancy_id: int) -> SuccessfullRequestEntity:
        pass
