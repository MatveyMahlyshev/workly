from pydantic import Field

from .user import UserBase, UserCreate


class RecruiterBase(UserBase):
    pass


class RecruiterCreate(UserCreate):
    company: str = Field(min_length=2, max_length=100, default="Название компании")
    position: str = Field(min_length=2, max_length=100, default="Занимаемая должность")
