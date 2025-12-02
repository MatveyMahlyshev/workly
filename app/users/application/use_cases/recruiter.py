from ..interfaces.recruiter_repo import IUserRepository
from users.domain.entities import RecruiterEntity
from users.domain.exceptions import EmailAlreadyExists, PhoneAlreadyExists

from .base_user import BaseUserUseCase


class RecruiterUseCase(BaseUserUseCase):
    async def create_user(
        self,
        **user_data,
    ) -> RecruiterEntity:
        exists = await self.repo._user_exists(
            email=user_data["email"],
            phone=user_data["phone"],
        )
        if exists["email"]:
            raise EmailAlreadyExists()
        if exists["phone"]:
            raise PhoneAlreadyExists()

        user = RecruiterEntity(
            email=user_data["email"],
            surname=user_data["surname"],
            name=user_data["name"],
            patronymic=user_data["patronymic"],
            phone=user_data["phone"],
            password_hash=self._hash_password(password=user_data["password"]),
            company=user_data["company"],
            position=user_data["position"],
        )
        return await self.repo._create_user(entity=user)

    # async def delete_user()
