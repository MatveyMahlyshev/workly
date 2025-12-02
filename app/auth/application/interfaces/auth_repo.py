from abc import ABC, abstractmethod

from auth.domain.entities import AuthEntity, TokenEntity
from users.infrastructure.database.models import User


class IAuthRepo(ABC):

    @abstractmethod
    async def _login(self, entity: AuthEntity) -> TokenEntity:
        pass

    @abstractmethod
    def _refresh(self, *args) -> str:
        pass

    @abstractmethod
    def _validate_password(self, password: str, hashed_pasword: str) -> bool:
        pass

    @abstractmethod
    async def _get_user(self, entity: AuthEntity) -> User | None:
        pass
