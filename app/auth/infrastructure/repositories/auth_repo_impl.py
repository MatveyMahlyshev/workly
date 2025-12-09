from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.orm import load_only, joinedload
import bcrypt

from auth.application.interfaces import IAuthRepository
from auth.domain.entities import AuthEntity, TokenEntity
from shared.infrastructure.models import User


class AuthRepositoryImpl(IAuthRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    def validate_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    async def get_user(self, entity: AuthEntity) -> User | None:
        stmt = (
            select(User)
            .options(
                joinedload(User.candidate),
                joinedload(User.recruiter),
                load_only(User.email, User.password_hash),
            )
            .where(User.email == entity.email)
        )
        result: Result = await self.session.execute(statement=stmt)
        user: User = result.scalar_one_or_none()
        return user

    def login(
        self,
        access_token: str,
        refresh_token: str,
    ) -> TokenEntity:
        return TokenEntity(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def refresh(*args):
        pass
