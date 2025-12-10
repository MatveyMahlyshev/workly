from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import (
    String,
    CheckConstraint,
    Enum as SQLEnum,
    Text,
    Boolean,
    ForeignKey,
)
from typing import TYPE_CHECKING


from recruiting.domain.entities import Period, WorkExperience
from shared.infrastructure.base import Base


if TYPE_CHECKING:
    from shared.infrastructure.models import Recruiter
    from .vacancy_skill_association import VacancySkillAssociation


class Vacancy(Base):
    __tablename__ = "vacancies"

    company: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(100))
    min_salary: Mapped[int | None] = mapped_column(
        default=None,
        nullable=True,
    )
    max_salary: Mapped[int | None] = mapped_column(
        default=None,
        nullable=True,
    )
    salary_period: Mapped[Period] = mapped_column(
        SQLEnum(Period),
        default=Period.MONTH,
        nullable=True,
    )
    experience: Mapped[WorkExperience] = mapped_column(
        SQLEnum(WorkExperience),
        default=WorkExperience.NO_EXPERIENCE,
    )
    description: Mapped[str] = mapped_column(
        Text,
        default=None,
        nullable=True,
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    recruiter_id: Mapped[int] = mapped_column(
        ForeignKey("recruiters.id"),
        unique=False,
    )

    recruiter: Mapped["Recruiter"] = relationship(
        "Recruiter", back_populates="vacancies"
    )

    skills: Mapped[list["VacancySkillAssociation"]] = relationship(
        back_populates="vacancy",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
