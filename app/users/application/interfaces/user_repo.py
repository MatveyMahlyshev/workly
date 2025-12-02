from abc import ABC, abstractmethod

from users.domain.entities import RecruiterEntity, CandidateEntity


class IUserRepository(ABC):
    @abstractmethod
    async def _create_user(self, entity: RecruiterEntity | CandidateEntity) -> None:
        pass

    @abstractmethod
    async def _delete_user(self) -> None:
        pass

    @abstractmethod
    async def _user_exists(self, email: str | None, phone: str | None) -> dict:
        pass
