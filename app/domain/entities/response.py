from dataclasses import dataclass


@dataclass
class SuccessResponseEntity:
    message: str = "success"