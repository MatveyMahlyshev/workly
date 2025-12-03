from pydantic import BaseModel, ConfigDict, Field


class ExperienceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    company: str = Field(
        min_length=2,
        max_length=100,
    )
    description: str | None = Field(min_length=2)


class Experience(ExperienceBase):
    pass
