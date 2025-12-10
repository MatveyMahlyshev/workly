from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from shared.infrastructure.base import Base

if TYPE_CHECKING:
    from .skill import Skill
    from .vacancy import Vacancy


class VacancySkillAssociation(Base):
    __tablename__ = "vacancy_skill_association"
    __table_args__ = (
        UniqueConstraint(
            "vacancy_id",
            "skill_id",
            name="idx_unique_vacancy_skill",
        ),
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey(
            "vacancies.id",
            ondelete="CASCADE",
        )
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey(
            "skills.id",
            ondelete="CASCADE",
        )
    )

    vacancy: Mapped["Vacancy"] = relationship(back_populates="skills")
    skill: Mapped["Skill"] = relationship(back_populates="vacancies")
