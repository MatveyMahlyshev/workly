from dataclasses import dataclass


@dataclass
class TokenEntity:
    access_token: str = ""
    refresh_token: str | None = ""
    token_type: str = "bearer"
