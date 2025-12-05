from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from shared.infrastructure.models.base import Base
from .user import User
from .mixins import UserRelationMixin


class Recruiter(UserRelationMixin, Base):
    position: Mapped[str] = mapped_column(String(100))
