from pydantic import BaseModel, ConfigDict, Field
from shared.presentation.schemas.validators import create_text_validator


class EducationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    educational_institution_title: str = Field(min_length=2, max_length=100)
    stage: str | None = Field(min_length=2, max_length=20)
    direction: str | None = Field(min_length=2, max_length=100)

    validate_title = create_text_validator(
        ["educational_institution_title"],
        with_digits=False,
        to_lower=False,
    )

    validate_stage = create_text_validator(
        ["stage"],
        with_digits=False,
        to_lower=True,
    )

    validate_direction = create_text_validator(
        ["direction"],
        with_digits=True,
        to_lower=False,
    )


class Education(EducationBase):
    pass
