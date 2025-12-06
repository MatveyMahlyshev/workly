from datetime import date

from .user import UserBase, UserCreate
from .education import Education
from .experience import Experience


class CandidateBase(UserBase):
    pass


class CandidateCreate(UserCreate):
    birth_date: date
    about_candidate: str | None = None
    location: str | None = None
    work_experience: list[Experience] | None = None
    education: list[Education] | None = None


class CandidateGet(UserBase):
    birth_date: date
    about_candidate: str
    location: str
    work_experience: list[Experience]
    education: list[Education]
