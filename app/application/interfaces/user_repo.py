from abc import ABC, abstractmethod

from domain.entities import RecruiterEntity, CandidateEntity


class IUserRepository(ABC):
    @abstractmethod
    async def _create_user(
        self, entity: RecruiterEntity | CandidateEntity
    ) -> RecruiterEntity | CandidateEntity:
        pass

    @abstractmethod
    async def _get_user_by_email(
        self, email: str
    ) -> RecruiterEntity | CandidateEntity | None:
        pass

    @abstractmethod
    async def _get_user_by_phone(
        self, phone: str
    ) -> RecruiterEntity | CandidateEntity | None:
        pass

    @abstractmethod
    async def _delete_user(self) -> None:
        pass
