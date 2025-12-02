from auth.application.interfaces import IAuthRepo
from auth.domain.entities import AuthEntity
from auth.domain.exceptions import UserNotFound, InvalidLoginData


class AuthUseCases:
    def __init__(self, repo: IAuthRepo):
        self.repo = repo

    async def login(self, login_data: AuthEntity):
        user = await self.repo.get_user(entity=login_data)
        if not user:
            raise UserNotFound()
        if not self.repo.validate_password(
            password=login_data.password,
            hashed_password=user.password_hash,
        ):
            raise InvalidLoginData()
        return await self.repo.login(entity=login_data)
