from abc import ABC, abstractmethod

from domain.entities import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: UserEntity) -> UserEntity:
        pass

    # @abstractmethod
    # async def delete_user(self, payload: dict) -> None:
    #     pass
