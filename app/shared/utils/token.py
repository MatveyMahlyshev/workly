from shared.infrastructure import TokenTypeFields


def validate_token_type(payload: dict, token_type: str) -> bool:
    if payload.get(TokenTypeFields.TOKEN_TYPE_FIELD) == token_type:
        return True
    return False
