from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload, selectinload, load_only

from users.domain.exceptions import CreateObjectException
from users.infrastructure.database.models import Recruiter, User
from users.domain.entities import RecruiterEntity, PermissionLevel
from users.application.interfaces import IRecruiterRepository
from .user_repo_mixin import UserRepoMixin
from shared.domain.entities import SuccessfullRequestEntity


class SQLRecruiterRepositoryImpl(UserRepoMixin, IRecruiterRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    def _to_entity(self, model: User) -> RecruiterEntity:
        return RecruiterEntity(
            id=model.id,
            surname=model.surname,
            name=model.name,
            patronymic=model.patronymic,
            email=model.email,
            phone=model.phone,
            position=model.recruiter.position,
        )

    def _to_model(self, entity: RecruiterEntity):
        user = User(
            email=entity.email,
            surname=entity.surname,
            name=entity.name,
            patronymic=entity.patronymic,
            phone=entity.phone,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            permission_level=PermissionLevel.RECRUITER.value,
        )
        recruiter = Recruiter(
            company=entity.company, position=entity.position, user=user
        )
        return user, recruiter

    async def user_exists(self, email: str = None, phone: str = None):
        return await super()._user_exists(email=email, phone=phone)

    async def create_user(self, entity: RecruiterEntity) -> SuccessfullRequestEntity:

        user_model, recruiter_model = self._to_model(entity=entity)

        try:
            self.session.add(user_model)
            self.session.add(recruiter_model)
            await self.session.commit()

        except IntegrityError:
            await self.session.rollback()
            raise CreateObjectException()

        return SuccessfullRequestEntity()

    async def get_profile(self, payload: dict) -> RecruiterEntity | None:
        stmt = (
            select(User)
            .options(
                joinedload(User.recruiter).load_only(Recruiter.position),
                load_only(
                    User.surname, User.name, User.patronymic, User.email, User.phone
                ),
            )
            .where(User.email == payload.get("sub"))
        )

        result: Result = await self.session.execute(statement=stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None
        return self._to_entity(model=user)

    """{
  "surname": "String",
  "email": "usqeer@example.com",
  "patronymic": "String",
  "is_active": true,
  "id": 65,
  "phone": "71244567890",
  "name": "String",
  "password_hash": "$2b$12$Uvto6u4g.Lbi4v/C7iqkFeH5xK4QMJbaLoQe/LYvHp9lQfOWqZ5U.",
  "permission_level": 2,
  "recruiter": {
    "user_id": 65,
    "id": 24,
    "position": "string"
  }
}"""

    async def delete_user(self):
        pass
