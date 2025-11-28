from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import date
from api_v1.skills.schemas import SkillBase


class CandidateProfileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    patronymic: str | None = Field(max_length=50)
    about_candidate: str | None = None
    education: str | None = None
    birth_date: date
    work_experience: str | None = None


class GetCandidateProfileUser(CandidateProfileBase):
    email: EmailStr = Field(min_length=5, max_length=50)
    skills: list[SkillBase]


class PutCandidateProfile(CandidateProfileBase):
    pass
