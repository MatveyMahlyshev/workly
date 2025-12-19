from dataclasses import dataclass


@dataclass
class SkillAnswerEntity:
    id: int | None = None
    text: str = ""
    is_correct: bool = False


@dataclass
class SkillQuestionEntity:
    id: int = 0
    text: str = ""
    answers: list[SkillAnswerEntity] = None
