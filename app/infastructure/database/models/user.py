from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import TYPE_CHECKING, Optional

from domain.entities.user import PermissionLevel
from .base import Base

if TYPE_CHECKING:
    from .candidate import Candidate
    from .recruiter import Recruiter


class User(Base):

    email: Mapped[str] = mapped_column(
        String(254), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    permission_level: Mapped[PermissionLevel] = mapped_column(
        Integer, default=PermissionLevel.CANDIDATE.value
    )
    candidate: Mapped[Optional["Candidate"]] = relationship(
        "Candidate",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    recruiter: Mapped[Optional["Recruiter"]] = relationship(
        "Recruiter", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
