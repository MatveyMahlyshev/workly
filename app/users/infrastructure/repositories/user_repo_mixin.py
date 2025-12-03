from sqlalchemy import select, Result, literal
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import User


class UserRepoMixin:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _user_exists(self, email: str = None, phone: str = None) -> dict:
        stmt = select(
            select(literal(1))
            .where(User.email == email if email else False)
            .exists()
            .label("email_exists"),
            select(literal(1))
            .where(User.phone == phone if phone else False)
            .exists()
            .label("phone_exists"),
        )
        result: Result = await self.session.execute(stmt)
        row = result.first()

        return {
            "email": bool(row.email_exists) if email else False,
            "phone": bool(row.phone_exists) if phone else False,
        }
