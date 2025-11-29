from dataclasses import dataclass
from datetime import date, datetime

from .user import UserEntity, PermissionLevel


@dataclass
class CandidateEntity(UserEntity):
    birth_date: datetime = date.today()
    work_experience: str = ""
    education: str = ""
    about_candidate: str = ""
    permission_level = PermissionLevel.CANDIDATE.value
