__all__ = (
    "User",
    "Candidate",
    "Recruiter",
    "Education",
    "Experience",
    "PermissionLevel",
    "Skill",
    "Vacancy",
)

from recruiting.infrastructure.database.models import Skill, Vacancy
from users.infrastructure.database.models import (
    User,
    PermissionLevel,
    Candidate,
    Recruiter,
    Education,
    Experience,
)
