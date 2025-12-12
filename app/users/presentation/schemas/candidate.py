from datetime import date, timedelta
from pydantic import field_validator


from .user import UserBase, UserCreate
from .education import Education
from .experience import Experience
from shared.presentation.schemas.validators import (
    create_text_validator,
    create_big_text_validator,
)


class CandidateBase(UserBase):
    birth_date: date
    about_candidate: str | None = None
    location: str | None = None
    work_experience: list[Experience] | None = None
    education: list[Education] | None = None

    validate_location = create_text_validator(
        ["location"],
        with_digits=False,
        to_lower=False,
    )

    validate_about = create_text_validator(
        ["about_candidate"],
        with_digits=True,
        to_lower=False,
    )
    validate_description = create_big_text_validator(["about_candidate"])

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Birth date cannot be in the future")

        min_age = 18
        min_date = date.today() - timedelta(days=min_age * 365.25)
        if value > min_date:
            raise ValueError(f"User must be at least {min_age} years old")

        max_age = 100
        max_date = date.today() - timedelta(days=max_age * 365.25)
        if value < max_date:
            raise ValueError(f"Age can't be more than {max_age} years")
        return value


class CandidateCreate(CandidateBase, UserCreate):
    pass


class CandidateGet(CandidateBase):
    pass
