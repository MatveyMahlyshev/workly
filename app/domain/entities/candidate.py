from dataclasses import dataclass
from datetime import date, datetime

from . import User


@dataclass
class Candidate(User):
    birth_date: datetime = date.today()
    work_experience: str = ""
    education: str = ""
    about_candidate: str = ""
