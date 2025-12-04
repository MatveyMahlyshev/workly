from pydantic import BaseModel, ConfigDict, Field, field_validator


class SkillBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(min_length=1, max_length=100)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str):
        if not v.strip():
            raise ValueError("Skill title can't be empty")
        if not [char for char in v if char.isalpha()]:
            raise ValueError("Skill title can't contain only digits")
        return v


class SkillCreate(SkillBase):
    pass


class SkillGet(SkillBase):
    pass
