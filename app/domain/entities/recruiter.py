from dataclasses import dataclass

from .user import UserEntity


@dataclass
class RecruiterEntity(UserEntity):
    company: str = ""
    position: str = ""
    permission_level = 2
