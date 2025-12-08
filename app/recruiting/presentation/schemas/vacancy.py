from pydantic import ConfigDict, BaseModel

from recruiting.domain.entities import WorkExperience, Period, SkillEntity
from shared.presentation.schemas.validators import create_text_validator


class VacancyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    company: str
    min_salary: int | None = None
    max_salary: int | None = None
    salary_period: Period = Period.MONTH
    experience: WorkExperience = WorkExperience.NO_EXPERIENCE.value
    description: str | None = None
    skills: list[SkillEntity] | None = None

    validate_field = create_text_validator(["title", "company"])


class VacancyCreate(VacancyBase):
    pass
