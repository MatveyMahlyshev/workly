from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base import Base
from .user import User
from .mixins import UserRelationMixin


class Recruiter(UserRelationMixin, Base):
    company: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(100))
