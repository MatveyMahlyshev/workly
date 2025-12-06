from dataclasses import dataclass

from .user import UserEntity


@dataclass
class RecruiterEntity(UserEntity):
    position: str = ""
