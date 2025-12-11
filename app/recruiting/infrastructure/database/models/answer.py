from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

from shared.infrastructure.base import Base

if TYPE_CHECKING:
    from .question import Question


class Answer(Base):
    text: Mapped[str]
    is_correct: Mapped[bool]
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))

    question: Mapped["Question"] = relationship(
        "Question",
        back_populates="answers",
    )
