from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
import re


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class UserAuthSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return v
