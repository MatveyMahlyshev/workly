from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from shared.infrastructure.models.base import Base
from .candidate import Candidate


class Education(Base):
    educational_institution_title: Mapped[str] = mapped_column(String(100))
    stage: Mapped[str] = mapped_column(
        String(20),
        default=None,
        nullable=True,
    )
    direction: Mapped[str] = mapped_column(
        String(100),
        default=None,
        nullable=True,
    )
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"))

    candidate: Mapped["Candidate"] = relationship(
        "Candidate",
        back_populates="educations",
    )
