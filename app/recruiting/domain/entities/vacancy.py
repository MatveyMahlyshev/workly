from dataclasses import dataclass
from enum import StrEnum

from .skill import SkillEntity


class WorkExperience(StrEnum):
    NO_EXPERIENCE = "Без опыта"
    LESS_THAN_1 = "до года работы"
    FROM_1_TO_2 = "1-2 года работы"
    FROM_3_TO_6 = "от 3 до 6 лет"
    MORE_THAN_6 = "Более 6 лет"


class Period(StrEnum):
    MONTH = "месяц"
    YEAR = "год"
    HOUR = "час"


@dataclass
class VacancyEntity:
    id: int = 0
    title: str = ""
    company: str = ""
    min_salary: int | None = None
    max_salary: int | None = None
    salary_period: Period = Period.MONTH
    experience: WorkExperience = WorkExperience.NO_EXPERIENCE.value
    description: str | None = None
    skills: list[SkillEntity] | None = None
