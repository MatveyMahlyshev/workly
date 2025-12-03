from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, Result, literal

from ..database.models import User, Candidate, Education, Experience
from users.domain.entities import RecruiterEntity, CandidateEntity
from users.domain.exceptions import CreateObjectException


class UserRepo:
    async def _create_user(self, entity: RecruiterEntity | CandidateEntity) -> None:

        user_model: User
        candidate_model: Candidate
        experiences: list[Experience]
        educations: list[Education]
        user_model, candidate_model, experiences, educations = self._to_model(entity=entity)

        try:
            self.session.add(user_model)
            await self.session.flush()

            candidate_model.user_id = user_model.id
            self.session.add(candidate_model)
            await self.session.flush() 

            for experience in experiences:
                experience.candidate_id = candidate_model.id
                self.session.add(experience)

            for education in educations:
                education.candidate_id = candidate_model.id
                self.session.add(education)

            await self.session.commit()

        except IntegrityError:

            await self.session.rollback()
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
