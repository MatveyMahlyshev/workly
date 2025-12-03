from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from users.application.interfaces import ICandidateRepository
from users.domain.entities import CandidateEntity, PermissionLevel
from users.infrastructure.database.models import User, Candidate, Education, Experience
from users.domain.exceptions import CreateObjectException
from shared.domain.entities import SuccessfullRequestEntity
from .user_repo_mixin import UserRepoMixin



class SQLCandidateRepositoryImpl(UserRepoMixin, ICandidateRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    def _to_model(self, entity: CandidateEntity):
        user = User(
            email=entity.email,
            surname=entity.surname,
            name=entity.name,
            patronymic=entity.patronymic,
            phone=entity.phone,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            permission_level=PermissionLevel.CANDIDATE.value,
        )
        candidate = Candidate(
            birth_date=entity.birth_date,
            about_candidate=entity.about_candidate,
            location=entity.location,
            user=user,
        )
        educations = [
            Education(
                educational_institution_title=education[
                    "educational_institution_title"
                ],
                stage=education["stage"],
                direction=education["direction"],
                candidate=candidate,
            )
            for education in entity.education
        ]

        experiences = [
            Experience(
                company=experience["company"],
                description=experience["description"],
                candidate=candidate,
            )
            for experience in entity.work_experience
        ]
        return user, candidate, experiences, educations

    async def create_user(self, entity: CandidateEntity) -> None:

        user_model: User
        candidate_model: Candidate
        experiences: list[Experience]
        educations: list[Education]
        user_model, candidate_model, experiences, educations = self._to_model(
            entity=entity
        )

        try:
            self.session.add(user_model)
            self.session.add(candidate_model)
            await self.session.flush()

            for experience in experiences:
                self.session.add(experience)

            for education in educations:
                self.session.add(education)

            await self.session.commit()

        except IntegrityError:

            await self.session.rollback()
            raise CreateObjectException()

        return SuccessfullRequestEntity()

    def user_exists(self, email=None, phone=None):
        return super()._user_exists(email=email, phone=phone)

    def delete_user(self):
        pass
