from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import TYPE_CHECKING

from domain.entities.user import PermissionLevel
from .base import Base

if TYPE_CHECKING:
    from .candidate import Candidate


class User(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    surname: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50))
    patronymic: Mapped[str | None] = mapped_column(String(50), default="")
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    is_active: Mapped[bool]
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
