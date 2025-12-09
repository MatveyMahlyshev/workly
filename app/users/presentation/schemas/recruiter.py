from pydantic import Field

from .user import UserBase, UserCreate
from shared.presentation.schemas.validators import create_text_validator


class RecruiterBase(UserBase):
    position: str = Field(min_length=2, max_length=100)

    validate_position = create_text_validator(
        ["position"],
        with_digits=False,
        to_lower=False,
    )


class RecruiterCreate(UserCreate, RecruiterBase):
    pass


class RecruiterGet(RecruiterBase):
    pass
