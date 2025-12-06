from pydantic import Field

from .user import UserBase, UserCreate


class RecruiterBase(UserBase):
    position: str = Field(min_length=2, max_length=100)


class RecruiterCreate(RecruiterBase):
    pass


class RecruiterGet(RecruiterBase):
    pass
