from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload, joinedload, load_only

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

    def _to_entity(self, model: User) -> CandidateEntity:
        return CandidateEntity(
            id=model.id,
            surname=model.surname,
            name=model.name,
            patronymic=model.patronymic,
            phone=model.phone,
            birth_date=model.candidate.birth_date,
            about_candidate=model.candidate.about_candidate,
            location=model.candidate.location,
            work_experience=model.candidate.experiences,
            education=model.candidate.educations,
        )

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

    async def get_profile(self, payload: dict) -> CandidateEntity:
        email = payload.get("sub")
        stmt = (
            select(User)
            .options(
                joinedload(User.candidate).options(
                    selectinload(Candidate.educations).options(
                        load_only(
                            Education.educational_institution_title,
                            Education.stage,
                            Education.direction,
                        )
                    ),
                    selectinload(Candidate.experiences).options(
                        load_only(Experience.company, Experience.description)
                    ),
                    load_only(
                        Candidate.about_candidate,
                        Candidate.location,
                        Candidate.birth_date,
                    ),
                ),
                load_only(
                    User.surname,
                    User.name,
                    User.patronymic,
                    User.email,
                    User.phone,
                ),
            )
            .where(User.email == email)
        )
        result: Result = await self.session.execute(statement=stmt)
        user: User = result.scalar_one()
    
        return self._to_entity(model=user)

    async def user_exists(self, email=None, phone=None):
        return await super()._user_exists(email=email, phone=phone)

    def delete_user(self):
        pass
