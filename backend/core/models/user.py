from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum, String, Integer
from enum import IntEnum
from typing import TYPE_CHECKING

from . import Base

if TYPE_CHECKING:
    from .candidate_profile import CandidateProfile
    from .vacancy import Vacancy
    from .vacancy_response import VacancyResponse


class PermissionLevel(IntEnum):
    CANDIDATE = 1
    HR = 2
    ADMIN = 3


class User(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    is_active: Mapped[bool]
    permission_level: Mapped[PermissionLevel] = mapped_column(
        Integer, default=PermissionLevel.CANDIDATE.value
    )

    candidate_profile: Mapped["CandidateProfile"] = relationship(
        "CandidateProfile", back_populates="user", uselist=False
    )

    vacancy: Mapped[list["Vacancy"]] = relationship("Vacancy", back_populates="hr")
