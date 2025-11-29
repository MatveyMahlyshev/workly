from abc import ABC, abstractmethod

from domain.entities import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserEntity | None:
        pass

    @abstractmethod
    async def delete_user(self) -> None:
        pass
