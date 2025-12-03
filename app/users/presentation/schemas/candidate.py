from datetime import date

from .user import UserBase, UserCreate
from .education import Education
from .experience import Experience


class CandidateBase(UserBase):
    pass


class CandidateCreate(UserCreate):
    birth_date: date
    work_experience: list[Experience] | None = None
    education: list[Education] | None = None
    about_candidate: str | None = None
    location: str | None = None
