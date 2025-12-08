from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


from shared.infrastructure.base import Base


class Skill(Base):
    title: Mapped[str] = mapped_column(String(100), unique=True, index=True)
