from pydantic import BaseModel, ConfigDict, Field

from shared.presentation.schemas.validators import create_text_validator


class AnswerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str = Field(min_length=1)
    is_correct: bool


class Answer(AnswerBase):
    pass
