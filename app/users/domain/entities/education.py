from dataclasses import dataclass


@dataclass
class EducationEntity:
    educational_institution_title: str = ""
    stage: str | None = None
    direction: str | None = None
