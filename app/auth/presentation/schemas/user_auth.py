from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
import re


class UserAuth(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr
    password: str = Field(min_length=10, max_length=50, default="Stringstri11")

    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("The password must contain at least one uppercase letter")
        if not re.search(r"\d", value):
            raise ValueError("The password must contain at least one number.")
        return value
