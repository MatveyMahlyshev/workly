from ..interfaces.user_repo import IUserRepository
from domain.entities import UserEntity
from domain.exceptions import EmailAlreadyExists
from utils import hash_password


class UserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def create_user(
        self,
        **user_data,
    ) -> UserEntity:
        exists = await self.repo.get_user_by_email(email=user_data["email"])
        if exists:
            raise EmailAlreadyExists()
        user = UserEntity(
            surname=user_data["surname"],
            name=user_data["name"],
            patronymic=user_data["patronymic"],
            email=user_data["email"],
            password_hash=hash_password(password=user_data["password"]),
        )
        return await self.repo.create_user(user)

    # async def delete_user()
