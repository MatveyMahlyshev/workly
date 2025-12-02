from datetime import date

from .user import UserBase, UserCreate

class CandidateBase(UserBase):
    pass

class CandidateCreate(UserCreate):
    birth_date: date
    work_experience: str | None = None
    education: str | None = None
    about_candidate: str | None = None
    location: str | None = None
