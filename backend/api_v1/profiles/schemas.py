from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Annotated
from annotated_types import (
    MinLen,
    MaxLen,
)
from datetime import date

from api_v1.skills.schemas import SkillBase


class CandidateProfileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    patronymic: str = Field(min_length=2, max_length=50)
    about_candidate: str | None = None
    education: str | None = None
    birth_date: date
    work_experience: str | None = None


class CandidateProfile(CandidateProfileBase):
    id: int


class CandidateProfileCreate(CandidateProfileBase):
    email: EmailStr


class CandidateProfileUser(BaseModel):
    email: Annotated[EmailStr, MinLen(5), MaxLen(25)]
    name: Annotated[str, MinLen(2), MaxLen(50)]
    surname: Annotated[str, MinLen(2), MaxLen(50)]
    patronymic: Annotated[str, MinLen(2), MaxLen(50)]
    age: int
    about_candidate: str
    education: str
    skills: list[SkillBase]


class CandidateProfileUpdate(CandidateProfileUser):
    pass
