from abc import ABC, abstractmethod

from users.domain.entities import RecruiterEntity, CandidateEntity
from shared.domain.entities import SuccessfullRequestEntity


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(
        self, entity: RecruiterEntity | CandidateEntity
    ) -> SuccessfullRequestEntity:
        pass

    @abstractmethod
    async def get_profile(self, payload: dict) -> RecruiterEntity | CandidateEntity:
        pass

    @abstractmethod
    async def user_exists(self, email: str = None, phone: str = None) -> dict:
        pass

    @abstractmethod
    async def delete_user(self) -> None:
        pass
