from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING


from shared.infrastructure.base import Base

if TYPE_CHECKING:
    from .vacancy_skill_association import VacancySkillAssociation


class Skill(Base):
    title: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    vacancy_associations: Mapped[list["VacancySkillAssociation"]] = relationship(
        back_populates="skill",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
