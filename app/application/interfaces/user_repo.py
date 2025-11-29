from abc import ABC, abstractmethod

from domain.entities import User


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    # @abstractmethod
    # async def delete_user(self, payload: dict) -> None:
    #     pass
