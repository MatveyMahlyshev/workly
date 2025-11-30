from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, String, Date
from datetime import date, timedelta

from .base import Base
from .mixins import UserRelationMixin


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
    work_experience: Mapped[str | None] = mapped_column(Text, default=None)
    education: Mapped[str | None] = mapped_column(Text, default=None)
    about_candidate: Mapped[str | None] = mapped_column(Text, default=None)

    location: Mapped[str | None] = mapped_column(String(100), default=None)
