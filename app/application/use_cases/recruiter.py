from ..interfaces.recruiter_repo import IUserRepository
from domain.entities import RecruiterEntity
from domain.exceptions import EmailAlreadyExists, PhoneAlreadyExists
from utils import hash_password
from .base_user import BaseUserUseCase


class RecruiterUseCase(BaseUserUseCase):
    async def create_user(
        self,
        **user_data,
    ) -> RecruiterEntity:
        if await self.repo._get_user_by_email(email=user_data["email"]):
            raise EmailAlreadyExists()
        if await self.repo._get_user_by_phone(phone=user_data["phone"]):
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
        return await self.repo._create_user(user)

    # async def delete_user()
