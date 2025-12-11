from pydantic import BaseModel, ConfigDict, Field

from shared.presentation.schemas.validators import create_text_validator
from .answer import Answer


class QuestionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str = Field(min_length=2)

    validate_text = create_text_validator(
        ["text"],
        with_digits=True,
        to_lower=False,
    )

    answers: list[Answer]


class Question(QuestionBase):
    pass


class QuestionCreate(QuestionBase):
    pass
