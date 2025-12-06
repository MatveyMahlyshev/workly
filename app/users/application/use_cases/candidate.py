from .base_user import BaseUserUseCase
from users.domain.entities import CandidateEntity
from users.domain.exceptions import EmailAlreadyExists, PhoneAlreadyExists
from shared.domain.entities import SuccessfullRequestEntity
from shared.utils.token import validate_token_type
from shared.infrastructure import TokenTypeFields
from shared.domain.exceptions import (
    InvalidTokenType,
    UserNotFound,
    InvalidTokenStructure,
)


class CandidateUseCase(BaseUserUseCase):
    async def create_user(self, **user_data) -> SuccessfullRequestEntity:
        exists = await self.repo.user_exists(
            email=user_data["email"],
            phone=user_data["phone"],
        )

        if exists["email"]:
            raise EmailAlreadyExists()
        if exists["phone"]:
            raise PhoneAlreadyExists()

        user = CandidateEntity(
            surname=user_data["surname"],
            name=user_data["name"],
            patronymic=user_data["patronymic"],
            email=user_data["email"],
            phone=user_data["phone"],
            password_hash=self._hash_password(user_data["password"]),
            birth_date=user_data["birth_date"],
            work_experience=user_data["work_experience"],
            education=user_data["education"],
            about_candidate=user_data["about_candidate"],
            location=user_data["location"],
        )
        return await self.repo.create_user(entity=user)

    async def get_profile(self, payload: dict) -> CandidateEntity | None:
        if not payload.get("sub"):
            raise InvalidTokenStructure()
        if not validate_token_type(
            payload=payload, token_type=TokenTypeFields.ACCESS_TOKEN_TYPE
        ):
            raise InvalidTokenType()
        profile = await self.repo.get_profile(payload=payload)
        if not profile:
            raise UserNotFound()
        return profile
