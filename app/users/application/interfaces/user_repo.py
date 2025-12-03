from abc import ABC, abstractmethod

from users.domain.entities import RecruiterEntity, CandidateEntity
from shared.domain.entities import SuccessfullRequestEntity


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, entity: RecruiterEntity | CandidateEntity) -> SuccessfullRequestEntity:
        pass

    @abstractmethod
    async def delete_user(self) -> None:
        pass

    
