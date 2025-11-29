from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy import select

from application.interfaces.user_repo import IUserRepository
from infastructure.database.models import User as user_model
from domain.entities import (
    User as user_domain_entity,
    SuccessResponseEntity as success_response,
)


class UserRepositoryImpl(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _message_response(self) -> success_response:
        return success_response()

    def _to_entity(self, model: user_model) -> user_domain_entity:
        return user_domain_entity(
            surname=model.surname,
            name=model.name,
            patronymic=model.patronymic,
            email=model.email,
            password_hash=model.password_hash,
            is_active=model.is_active,
            permission_level=model.permission_level,
        )

    def _to_model(self, entity: user_domain_entity) -> user_model:
        return user_model(
            surname=entity.surname,
            name=entity.name,
            patronymic=entity.patronymic,
            email=entity.email,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            permission_level=2,
        )

    async def create_user(self, user_entity: user_domain_entity):
        user_exists = await self.session.execute(
            select(user_model).where(user_model.email == user_entity.email)
        )
        if user_exists.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        model = self._to_model(entity=user_entity)

        self.session.add(model)
        try:
            await self.session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Integrity error",
            )
        return self._message_response()
