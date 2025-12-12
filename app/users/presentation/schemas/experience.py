from pydantic import BaseModel, ConfigDict, Field

from shared.presentation.schemas.validators import (
    create_text_validator,
    create_big_text_validator,
)


class ExperienceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    company: str = Field(
        min_length=2,
        max_length=100,
    )
    description: str | None = None

    validate_description = create_big_text_validator(["description"])

    validate_company = create_text_validator(
        ["company"],
        with_digits=False,
        to_lower=False,
    )


class Experience(ExperienceBase):
    pass
