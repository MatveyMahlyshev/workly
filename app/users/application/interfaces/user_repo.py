from abc import ABC, abstractmethod

from users.domain.entities import RecruiterEntity, CandidateEntity


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, entity: RecruiterEntity | CandidateEntity) -> None:
        pass

    @abstractmethod
    async def delete_user(self) -> None:
        pass

    @abstractmethod
    async def user_exists(self, email: str | None, phone: str | None) -> dict:
        pass
