from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from users.domain.exceptions import CreateObjectException
from users.infrastructure.database.models import Recruiter, User
from users.domain.entities import RecruiterEntity, PermissionLevel
from users.application.interfaces import IRecruiterRepository
from .user_repo_mixin import UserRepoMixin
from shared.domain.entities import SuccessfullRequestEntity


class SQLRecruiterRepositoryImpl(UserRepoMixin, IRecruiterRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

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

    async def delete_user(self):
        pass
