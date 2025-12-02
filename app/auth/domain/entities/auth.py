from dataclasses import dataclass


@dataclass
class AuthEntity:
    email: str = ""
    password: str = ""
