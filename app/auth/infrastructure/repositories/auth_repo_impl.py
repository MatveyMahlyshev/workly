from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
import bcrypt

from auth.application.interfaces import IAuthRepo
from auth.domain.entities import AuthEntity, TokenEntity
from users.infrastructure.database.models import User
from .token_repo import TokenRepo, TokenTypeFields


class AuthRepositoryImpl(TokenRepo, IAuthRepo):

    def __init__(self, session: AsyncSession):
        self.session = session

    def _create_token(self, entity: AuthEntity, token_type: str):
        jwt_payload = {"sub": entity.email}
        return super()._create_token(token_type=token_type, token_data=jwt_payload)

    def _validate_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    async def _get_user(self, entity: AuthEntity) -> User | None:
        stmt = select(User).where(User.email == entity.email)
        result: Result = await self.session.execute(statement=stmt)
        user: User = result.scalar_one_or_none()
        return user

    async def _login(self, entity: AuthEntity) -> TokenEntity:
        access_token = self._create_token(
            entity=entity,
            token_type=TokenTypeFields.ACCESS_TOKEN_TYPE,
        )
        refresh_token = self._create_token(
            entity=entity,
            token_type=TokenTypeFields.REFRESH_TOKEN_TYPE,
        )
        return TokenEntity(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def _refresh(*args):
        pass
