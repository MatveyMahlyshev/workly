from pydantic import field_validator, ValidationInfo
import re


def check_didigts(value: str, field_name: str):
    if any(char.isdigit() for char in value):
        raise ValueError(f"{field_name} can't contain digits")


def check_only_didigts(value: str, field_name: str):
    if not any(char.isalpha() for char in value):
        raise ValueError(f"{field_name} can't contain only digits")


def check_empty(value: str, field_name: str):
    if not value:
        raise ValueError(f"{field_name} can't be empty")


def create_text_validator(fields: list[str], with_digits: bool, to_lower: bool):
    @field_validator(*fields)
    @classmethod
    def validator(cls, value: str, info: ValidationInfo):
        if value is None:
            return None
        field_name = info.field_name
        value = value.strip()

        check_empty(value=value, field_name=field_name)
        if not with_digits:
            check_didigts(value=value, field_name=field_name)
        check_only_didigts(value=value, field_name=field_name)

        if to_lower:
            value = value.lower()

        return value.capitalize()

    return validator


def create_big_text_validator(fields: list[str]):

    @field_validator(*fields)
    @classmethod
    def validator(cls, value: str, info: ValidationInfo):

        if value is None:
            return None

        value = value.strip()

        if len(value) == 0:
            return None
        field_name = info.field_name
        check_only_didigts(value=value, field_name=field_name)

        value = re.sub(r"\s+", " ", value)
        value = re.sub(r"\s+([.,!?:;])", r"\1", value)
        value = re.sub(r"([.!?])\1+", r"\1", value)
        value = re.sub(r"([.,!?:;])(?![.!?:;\s])", r"\1 ", value)

        sentences = re.split(r"([.!?])\s+", value)
        result = []

        for i in range(0, len(sentences), 2):
            if i < len(sentences):
                sentence = sentences[i]
                if sentence:
                    if sentence[0].islower():
                        sentence = sentence[0].upper() + sentence[1:]
                    result.append(sentence)

                if i + 1 < len(sentences):
                    result.append(sentences[i + 1] + " ")

        value = "".join(result).strip()

        if value and value[0].islower():
            value = value[0].upper() + value[1:]

        return value

    return validator
