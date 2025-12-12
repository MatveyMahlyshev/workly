from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING

from shared.infrastructure.base import Base

if TYPE_CHECKING:
    from .question import Question


class Answer(Base):
    __table_args__ = (
        UniqueConstraint(
            "text",
            "question_id",
            name="idx_unique_text_questionid",
        ),
    )
    text: Mapped[str]
    is_correct: Mapped[bool]
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))

    question: Mapped["Question"] = relationship(
        "Question",
        back_populates="answers",
    )
