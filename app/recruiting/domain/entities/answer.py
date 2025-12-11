from dataclasses import dataclass


@dataclass
class AnswerEntity:
    id: int | None = None
    text: str = ""
    is_correct: bool = False
