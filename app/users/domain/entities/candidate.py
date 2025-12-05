from dataclasses import dataclass
from datetime import date, datetime

from .user import UserEntity
from .education import EducationEntity
from .experience import ExperienceEntity


@dataclass
class CandidateEntity(UserEntity):
    birth_date: datetime = date.today()
    about_candidate: str | None = None
    location: str | None = None
    work_experience: list[ExperienceEntity] | None = None
    education: list[EducationEntity] | None = None
    