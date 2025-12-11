from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from shared.infrastructure.base import Base

if TYPE_CHECKING:
    from .answer import Answer


class Question(Base):
    text: Mapped[str]
    
    answers: Mapped[list["Answer"]] = relationship("Answer", back_populates="question",)
