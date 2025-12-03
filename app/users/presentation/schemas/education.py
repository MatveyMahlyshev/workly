from pydantic import BaseModel, ConfigDict, Field


class EducationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    educational_institution_title: str = Field(min_length=2, max_length=100)
    stage: str | None = Field(min_length=2, max_length=20)
    direction: str | None = Field(min_length=2, max_length=100)


class Education(EducationBase):
    pass
