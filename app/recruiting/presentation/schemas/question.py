from pydantic import BaseModel, ConfigDict, Field

from shared.presentation.schemas.validators import create_big_text_validator
from .answer import Answer


class QuestionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str = Field(min_length=2)

    validate_text = create_big_text_validator(
        ["text"],
    )

    answers: list[Answer]


class Question(QuestionBase):
    pass


class QuestionCreate(QuestionBase):
    pass
