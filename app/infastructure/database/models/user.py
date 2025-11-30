from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import TYPE_CHECKING

from domain.entities.user import PermissionLevel
from .base import Base

if TYPE_CHECKING:
    from .candidate import Candidate


class User(Base):

    email: Mapped[str] = mapped_column(
        String(254), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    permission_level: Mapped[PermissionLevel] = mapped_column(
        Integer, default=PermissionLevel.CANDIDATE.value
    )
    candidate: Mapped["Candidate"] = relationship(
        "Candidate",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
