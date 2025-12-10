from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    Field,
    EmailStr,
)
import re
import random
from typing import Annotated
from annotated_types import MinLen, MaxLen
from shared.presentation.schemas.validators import create_text_validator


def generate_phone_number() -> str:
    random_number = ""
    while len(random_number) != 10:
        random_number += str(random.randint(0, 9))
    return "7" + random_number


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    patronymic: str | None = Field(min_length=2, max_length=50, default=None)
    email: Annotated[EmailStr, MinLen(5), MaxLen(50)]
    phone: str = Field(min_length=10, max_length=20, default=generate_phone_number())

    validate_field = create_text_validator(
        ["name", "surname", "patronymic"],
        with_digits=False,
        to_lower=True,
    )

    @field_validator("phone")
    @classmethod
    def phone_number_validation(cls, value: str) -> str:
        if any(char.isalpha() for char in value):
            raise ValueError("Invalid phone number")
        valid_number = "".join(filter(str.isdigit, value))
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
    password: str = Field(
        min_length=10,
        max_length=50,
        default="Stringstri11",
    )

    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("The password must contain at least one capital letter")
        if not re.search(r"\d", value):
            raise ValueError("The password must contain at least one number")
        return value
