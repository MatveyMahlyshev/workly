from dataclasses import dataclass

from .answer import AnswerEntity


@dataclass
class QuestionEntity:
    id: int = 0
    text: str = ""
    answers: list[AnswerEntity] = None
