from auth import dependencies, utils


def test_create_access_token():
    jwt_payload = {"sub": "test@example.com"}
    access_token = dependencies.create_token(
        token_type="access",
        token_data=jwt_payload,
    )
    decoded_jwt = utils.decode_jwt(access_token)
    assert decoded_jwt.get("sub")
    assert decoded_jwt.get("exp")
    assert decoded_jwt.get("iat")
    assert decoded_jwt.get("type")
    assert decoded_jwt.get("sub") == jwt_payload.get("sub")
    assert decoded_jwt.get("type") == "access"


def test_create_refresh_token():
    jwt_payload = {"sub": "test@example.com"}
    refresh_token = dependencies.create_token(
        token_type="refresh",
        token_data=jwt_payload,
    )
    decoded_jwt = utils.decode_jwt(refresh_token)
    assert decoded_jwt.get("sub")
    assert decoded_jwt.get("exp")
    assert decoded_jwt.get("iat")
    assert decoded_jwt.get("type")
    assert decoded_jwt.get("sub") == jwt_payload.get("sub")
    assert decoded_jwt.get("type") == "refresh"


def test_validate_token_type():
    jwt_payload = {"sub": "test@example.com", "type": "access"}
    assert dependencies.validate_token_type(payload=jwt_payload, token_type="access")
