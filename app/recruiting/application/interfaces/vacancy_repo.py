from abc import ABC, abstractmethod


from recruiting.domain.entities import VacancyEntity
from shared.domain.entities import SuccessfullRequestEntity


class IVacancyRepository(ABC):

    @abstractmethod
    async def create_vacancy(
        self, payload: dict, entity: VacancyEntity
    ) -> SuccessfullRequestEntity:
        pass

    @abstractmethod
    async def get_vacancy(self, vacancy_id: int) -> VacancyEntity:
        pass

    @abstractmethod
    async def delete_vacancy(self, vacancy_id: int) -> None:
        pass
