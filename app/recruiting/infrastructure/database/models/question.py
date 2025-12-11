from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING

from shared.infrastructure.base import Base

if TYPE_CHECKING:
    from .answer import Answer
    from .skill import Skill


class Question(Base):
    __table_args__ = (
        UniqueConstraint("text", "skill_id", name="idx_unique_text_skillid"),
    )
    
    text: Mapped[str]
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))

    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="question",
    )

    skill: Mapped["Skill"] = relationship("Skill", back_populates="questions")
