from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, Date
from datetime import date, timedelta
from typing import TYPE_CHECKING

from .base import Base
from .mixins import UserRelationMixin


if TYPE_CHECKING:
    from .experience import Experience
    from .education import Education


def default_18_years_ago():
    return date.today() - timedelta(days=18 * 365)


class Candidate(UserRelationMixin, Base):

    _user_back_populates = "candidate"
    _user_id_unique: bool = True

    birth_date: Mapped[date] = mapped_column(
        Date,
        default=default_18_years_ago,
        nullable=False,
    )
    about_candidate: Mapped[str | None] = mapped_column(
        Text, default=None, nullable=True
    )

    location: Mapped[str | None] = mapped_column(
        String(100), default=None, nullable=True
    )

    experiences: Mapped[list["Experience"]] = relationship(
        "Experience",
        back_populates="candidate",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    educations: Mapped[list["Education"]] = relationship(
        "Education",
        back_populates="candidate",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
