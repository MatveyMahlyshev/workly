from sqlalchemy.ext.asyncio import AsyncSession

from users.application.interfaces import ICandidateRepository
from users.domain.entities import CandidateEntity
from users.infrastructure.database.models import User, Candidate
from .user_repo import UserRepo


class CandidateRepositoryImpl(UserRepo, ICandidateRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_model(self, entity: CandidateEntity):
        user = User(
            email=entity.email,
            surname=entity.surname,
            name=entity.name,
            patronymic=entity.patronymic,
            phone=entity.phone,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            permission_level=1,
        )
        candidate = Candidate(
            birth_date=entity.birth_date,
            work_experience=entity.work_experience,
            education=entity.education,
            about_candidate=entity.about_candidate,
            location=entity.location,
        )
        return user, candidate

    def create_user(self, entity):
        return super()._create_user(entity=entity)

    def user_exists(self, email=None, phone=None):
        return super()._user_exists(email=email, phone=phone)

    def delete_user(self):
        pass
