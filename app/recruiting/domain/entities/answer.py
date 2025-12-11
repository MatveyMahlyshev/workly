from dataclasses import dataclass


@dataclass
class AnswerEntity:
    id: int = 0
    text: str = ""
    is_correct: bool = False