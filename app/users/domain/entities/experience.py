from dataclasses import dataclass


@dataclass
class ExperienceEntity:
    company: str = ""
    description: str | None = None
