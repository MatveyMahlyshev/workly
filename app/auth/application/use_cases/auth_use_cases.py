from auth.application.interfaces import IAuthRepository, ITokenRepository
from auth.domain.entities import AuthEntity
from auth.domain.exceptions import UserNotFound, InvalidLoginData


class AuthUseCases:
    def __init__(self, auth_repo: IAuthRepository, token_repo: ITokenRepository):
        self.auth_repo = auth_repo
        self.token_repo = token_repo

    async def login(self, login_data: AuthEntity):
        user = await self.auth_repo.get_user(entity=login_data)
        if not user:
            raise UserNotFound()
        if not self.auth_repo.validate_password(
            password=login_data.password,
            hashed_password=user.password_hash,
        ):
            raise InvalidLoginData()
        access_token = self.token_repo.create_token(
            token_data={"sub": login_data.email}, token_type="access"
        )
        refresh_token = self.token_repo.create_token(
            token_data={"sub": login_data.email}, token_type="refresh"
        )
        return await self.auth_repo.login(
            access_token=access_token, refresh_token=refresh_token
        )
