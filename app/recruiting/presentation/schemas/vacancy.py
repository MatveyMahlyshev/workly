from pydantic import ConfigDict, BaseModel, field_validator

from recruiting.domain.entities import WorkExperience, Period, SkillEntity
from shared.presentation.schemas.validators import (
    create_text_validator,
    create_big_text_validator,
)
from datetime import datetime
from .skill import Skill


class VacancyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    company: str
    min_salary: int | None = None
    max_salary: int | None = None
    salary_period: Period = Period.MONTH
    experience: WorkExperience = WorkExperience.NO_EXPERIENCE.value
    description: str | None = None
    skills: list[Skill] | None = None

    validate_field = create_text_validator(
        ["title", "company"],
        with_digits=False,
        to_lower=False,
    )
    validate_description = create_big_text_validator(["description"])

    @field_validator("max_salary")
    @classmethod
    def validate_salary(cls, value, info):
        if value is not None:
            min_salary = info.data.get("min_salary")
            if min_salary is None:
                return value
            if min_salary > value:
                raise ValueError("min_salary must be <= max_salary")
        return value

    @field_validator("min_salary", "max_salary")
    @classmethod
    def validate_min_max_salary(cls, value):
        if value is None or value <= 0:
            return None
        return value

    @field_validator("skills")
    @classmethod
    def validate_skills(cls, value: list[Skill]):
        skills = set()
        return [
            skill
            for skill in value
            if skill.title not in skills and not skills.add(skill.title)
        ]


class VacancyCreate(VacancyBase):
    pass


class VacancyGet(VacancyBase):
    id: int
    created_at: datetime


class VacancyRecruiterGet(VacancyGet):
    is_published: bool
