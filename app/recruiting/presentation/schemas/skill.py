from pydantic import BaseModel, ConfigDict, Field
from shared.presentation.schemas.validators import create_text_validator


class SkillBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(min_length=1, max_length=100)

    validate_field = create_text_validator(["title"])


class SkillCreate(SkillBase):
    pass


class SkillGet(SkillBase):
    pass
