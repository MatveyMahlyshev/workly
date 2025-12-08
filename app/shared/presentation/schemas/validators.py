from pydantic import field_validator, ValidationInfo


def create_text_validator(fields: list[str]):

    @field_validator(*fields)
    @classmethod
    def validator(cls, value: str, info: ValidationInfo):
        if value is None:
            return None

        field_name = info.field_name
        value = value.strip()

        if not value:
            raise ValueError(f"{field_name} can't be empty")
        if not any(char.isalpha() for char in value):
            raise ValueError(f"{field_name} can't contain only digits")

        return value.capitalize()

    return validator
