from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey

from shared.infrastructure.models.base import Base
from .candidate import Candidate


class Experience(Base):
    company: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(
        Text,
        default=None,
        nullable=True,
    )
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"))
    candidate: Mapped["Candidate"] = relationship(
        "Candidate",
        back_populates="experiences",
    )
