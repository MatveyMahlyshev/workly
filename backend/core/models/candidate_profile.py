from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import (
    String,
    Text,
    Date,
)
from typing import TYPE_CHECKING
from datetime import date, timedelta


from . import Base
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .candidate_profile_skill_association import CandidateProfileSkillAssociation
    from .vacancy_response import VacancyResponse


def default_18_years_ago():
    return date.today() - timedelta(days=18 * 365)


class CandidateProfile(UserRelationMixin, Base):
    __tablename__ = "candidate_profiles"

    _user_back_populates = "candidate_profile"
    _user_id_unique: bool = True

    surname: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50))
    patronymic: Mapped[str | None] = mapped_column(String(50))
    birth_date: Mapped[date] = mapped_column(
        Date,
        default=default_18_years_ago,
        nullable=False,
    )
    work_experience: Mapped[str | None] = mapped_column(Text, default="")
    education: Mapped[str | None] = mapped_column(Text, default="")
    about_candidate: Mapped[str | None] = mapped_column(Text, default="")

    profile_skills: Mapped[list["CandidateProfileSkillAssociation"]] = relationship(
        back_populates="candidate_profile"
    )

    vacancy_responses: Mapped[list["VacancyResponse"]] = relationship(
        back_populates="candidate_profile"
    )
