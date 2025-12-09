from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

from shared.infrastructure.base import Base
from .user import User
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from shared.infrastructure.models import Vacancy


class Recruiter(UserRelationMixin, Base):
    position: Mapped[str] = mapped_column(String(100))

    vacancies: Mapped[list["Vacancy"]] = relationship(
        "Vacancy",
        back_populates="recruiter",
    )
