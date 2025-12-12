from pydantic import BaseModel, ConfigDict, Field

from shared.presentation.schemas.validators import create_big_text_validator


class AnswerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str = Field(min_length=1)
    is_correct: bool

    validate_text = create_big_text_validator(
        ["text"],
    )


class Answer(AnswerBase):
    pass
