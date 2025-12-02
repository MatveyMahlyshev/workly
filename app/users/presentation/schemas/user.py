from pydantic import BaseModel, ConfigDict, field_validator, Field, EmailStr
import re
from typing import Annotated
from annotated_types import MinLen, MaxLen


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    patronymic: str | None = Field(min_length=2, max_length=50, default=None)
    email: Annotated[EmailStr, MinLen(5), MaxLen(50)]
    phone: str = Field(min_length=10, max_length=20, default="71234567890")

    @field_validator("name", "surname", "patronymic")
    @classmethod
    def capitalize_names(cls, v: str | None) -> str | None:
        if v and isinstance(v, str):
            return v.strip().lower().capitalize()
        return v

    @field_validator("phone")
    @classmethod
    def phone_number_validation(cls, v: str) -> str:
        if any(char.isalpha() for char in v):
            raise ValueError("Invalid phone number")
        valid_number = "".join(filter(str.isdigit, v))
        length_of_number = len(valid_number)
        if (length_of_number < 10 or length_of_number > 11) or (
            (length_of_number == 11) and (valid_number[0] not in ["7", "8"])
        ):
            raise ValueError("Invalid phone number")
        elif length_of_number == 11:
            valid_number = "7" + valid_number[1:]
        elif length_of_number == 10:
            valid_number = "7" + valid_number
        return valid_number


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
