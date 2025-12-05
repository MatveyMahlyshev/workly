from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, CheckConstraint, Enum as SQLEnum, Text, Boolean
from recruiting.domain.entities import Period, WorkExperience

from shared.infrastructure.models import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    __table_args__ = (
        CheckConstraint("min_salary >= 0", name="min_salary_non_negative"),
        CheckConstraint(
            "max_salary IS NULL OR max_salary >= 0", name="max_salary_non_negative"
        ),
        CheckConstraint(
            "max_salary IS NULL OR max_salary >= min_salary",
            name="min_not_greater_than_max",
        ),
    )
    # recruiter_id: int
    company: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(100))
    min_salary: Mapped[int | None] = mapped_column(default=None, nullable=True)
    max_salary: Mapped[int | None] = mapped_column(default=None, nullable=True)
    salary_period: Mapped[Period] = mapped_column(
        SQLEnum(Period), default=Period.MONTH, nullable=True
    )
    experience: Mapped[WorkExperience] = mapped_column(
        SQLEnum(WorkExperience), default=WorkExperience.NO_EXPERIENCE
    )
    description: Mapped[str] = mapped_column(Text, default=None, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
