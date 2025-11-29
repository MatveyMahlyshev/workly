from pydantic import BaseModel, ConfigDict, field_validator, Field, EmailStr
import re
from typing import Annotated
from annotated_types import MinLen, MaxLen


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(min_length=2, max_length=50, default="Имя")
    surname: str = Field(min_length=2, max_length=50, default="Фамилия")
    patronymic: str | None = Field(max_length=50, default="Отчество")
    email: Annotated[EmailStr, MinLen(5), MaxLen(50)]

    @field_validator("name", "surname", "patronymic")
    @classmethod
    def capitalize_names(cls, v: str | None) -> str | None:
        if v and isinstance(v, str):
            return v.strip().lower().capitalize()
        return v

class User(UserBase):
    id: int


class UserCreate(UserBase):
    password: str = Field(min_length=10, max_length=50, default="Stringstri11")

    @field_validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return v
