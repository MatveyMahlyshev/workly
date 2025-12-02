from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, Result, literal

from ..database.models import User
from users.domain.entities import RecruiterEntity, CandidateEntity
from users.domain.exceptions import CreateObjectException


class UserRepo:
    async def _create_user(self, entity: RecruiterEntity | CandidateEntity) -> None:

        user_model, type_model = self._to_model(entity=entity)

        try:
            self.session.add(user_model)
            await self.session.flush()

            type_model.user_id = user_model.id
            self.session.add(type_model)

            await self.session.commit()

        except IntegrityError as e:

            await self.session.rollback()
            print(e)
            raise CreateObjectException()

        return None

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
