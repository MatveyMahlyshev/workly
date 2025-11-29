from ..interfaces.user_repo import IUserRepository
from domain.entities import User
from utils import hash_password


class UserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def create_user(
        self,
        surname: str,
        name: str,
        patronymic: str,
        email: str,
        password: str,
    ) -> User:
        user = User(
            surname=surname,
            name=name,
            patronymic=patronymic,
            email=email,
            password_hash=hash_password(password=password),
        )
        return await self.repo.create_user(user)

    # async def delete_user()
