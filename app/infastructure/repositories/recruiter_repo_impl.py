from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload

from domain.exceptions import EmailAlreadyExists
from infastructure.database.models import Recruiter, User
from domain.entities import RecruiterEntity
from application.interfaces import IUserRepository


class RecruiterRepositoryImpl(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _user_model_to_recruiter_entity(
        self, model: User | Recruiter
    ) -> RecruiterEntity:
        if isinstance(model, User):
            return RecruiterEntity(
                email=model.email,
                password_hash=model.password_hash,
                is_active=model.is_active,
                permission_level=model.permission_level,
                company=model.recruiter.company,
                position=model.recruiter.position,
                surname=model.recruiter.surname,
                name=model.recruiter.name,
                patronymic=model.recruiter.patronymic,
                phone=model.recruiter.phone,
            )
        if isinstance(model, Recruiter):
            return RecruiterEntity(
                email=model.user.email,
                password_hash=model.user.password_hash,
                is_active=model.user.is_active,
                permission_level=model.user.permission_level,
                company=model.company,
                position=model.position,
                surname=model.surname,
                name=model.name,
                patronymic=model.patronymic,
                phone=model.phone,
            )

    def _to_entity(
        self, recruiter_model: Recruiter, user_model: User
    ) -> RecruiterEntity:
        return RecruiterEntity(
            email=user_model.email,
            password_hash=user_model.password_hash,
            is_active=user_model.is_active,
            permission_level=user_model.permission_level,
            company=recruiter_model.company,
            position=recruiter_model.position,
            surname=recruiter_model.surname,
            name=recruiter_model.name,
            patronymic=recruiter_model.patronymic,
            phone=recruiter_model.phone,
        )

    def _to_model(self, entity: RecruiterEntity):
        user = User(
            email=entity.email,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            permission_level=2,
        )
        recruiter = Recruiter(
            company=entity.company,
            position=entity.position,
            surname=entity.surname,
            name=entity.name,
            patronymic=entity.patronymic,
            phone=entity.phone,
        )
        return user, recruiter

    async def _create_user(self, recruiter_entity: RecruiterEntity) -> None:
        user_model, recruiter_model = self._to_model(entity=recruiter_entity)
        try:
            self.session.add(user_model)
            await self.session.flush()
            recruiter_model.user_id = user_model.id
            self.session.add(recruiter_model)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise EmailAlreadyExists

        return None

    async def _get_user_by_email(self, email) -> RecruiterEntity | None:
        stmt = (
            select(User)
            .options(selectinload(User.recruiter))
            .where(User.email == email)
        )
        result: Result = await self.session.execute(statement=stmt)
        user: User = result.scalar_one_or_none()
        print(user)
        if user:
            return self._user_model_to_recruiter_entity(model=user)
        return None

    async def _get_user_by_phone(self, phone: str) -> RecruiterEntity | None:
        stmt = (
            select(Recruiter)
            .options(selectinload(Recruiter.user))
            .where(Recruiter.phone == phone)
        )
        result: Result = await self.session.execute(statement=stmt)
        recruiter: Recruiter = result.scalar_one_or_none()
        if recruiter:
            return self._user_model_to_recruiter_entity(model=recruiter)
        return None

    async def _delete_user(self):
        pass
