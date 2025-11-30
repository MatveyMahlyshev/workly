from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, Result


from application.interfaces.user_repo import IUserRepository
from infastructure.database.models import User
from domain.entities import UserEntity
from domain.exceptions import EmailAlreadyExists


class UserRepositoryImpl(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: User) -> UserEntity:
        return UserEntity(
            surname=model.surname,
            name=model.name,
            patronymic=model.patronymic,
            email=model.email,
            password_hash=model.password_hash,
            is_active=model.is_active,
            permission_level=model.permission_level,
        )

    def _to_model(self, entity: UserEntity) -> User:
        return User(
            surname=entity.surname,
            name=entity.name,
            patronymic=entity.patronymic,
            email=entity.email,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            permission_level=2,
        )

    async def create_user(self, user_entity: UserEntity) -> UserEntity:
        model = self._to_model(entity=user_entity)
        try:
            self.session.add(model)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise EmailAlreadyExists

        return self._to_entity(model=model)

    async def get_user_by_email(self, email) -> UserEntity | None:
        stmt = select(User).where(User.email == email)
        result: Result = await self.session.execute(statement=stmt)
        user = result.scalar_one_or_none()
        if user:
            return self._to_entity(model=user)
        return None

    async def delete_user(self):
        pass
