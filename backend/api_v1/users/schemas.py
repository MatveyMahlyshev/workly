from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
import re
from typing import Annotated
from annotated_types import MinLen, MaxLen

from api_v1.profiles.schemas import CandidateProfileCreate


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: Annotated[EmailStr, MinLen(5), MaxLen(50)]


class User(UserBase):
    id: int


class UserCreate(UserBase):
    password: str = Field(min_length=10, max_length=50)

    @field_validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return v


class UserUpdate(UserCreate):
    pass


class CreateUserWithProfile(UserCreate, CandidateProfileCreate):
    # user: UserCreate
    # profile: CandidateProfileBase
    pass
