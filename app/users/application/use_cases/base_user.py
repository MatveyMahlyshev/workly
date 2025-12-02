from abc import ABC, abstractmethod

from users.application.interfaces import PasswordHasher, IUserRepository


class BaseUserUseCase(ABC):
    def __init__(
        self,
        repo: IUserRepository,
        password_hasher: PasswordHasher,
    ):
        self.repo = repo
        self.password_hasher = password_hasher

    def _hash_password(self, password: str) -> str:
        return self.password_hasher.hash(password=password)

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return self.password_hasher.verify(
            password=password,
            hashed_password=hashed_password,
        )
