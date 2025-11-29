from dataclasses import dataclass
from enum import IntEnum


class PermissionLevel(IntEnum):
    CANDIDATE = 1
    HR = 2
    ADMIN = 3


@dataclass
class UserEntity:
    surname: str = ""
    name: str = ""
    patronymic: str = ""
    email: str = ""
    password_hash: str = ""
    is_active: bool = True
    permission_level: PermissionLevel = PermissionLevel.HR.value

    def set_password(self, password_hash: str) -> None:
        if len(password_hash) != 60:
            raise ValueError("Invalid hash")
        self.password_hash = password_hash
