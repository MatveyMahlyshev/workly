from datetime import timedelta, datetime, timezone
import jwt


from auth.application.interfaces import ITokenRepo
from config.settings import settings


class TokenTypeFields:
    TOKEN_TYPE_FIELD = "type"
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"


class TokenRepoImpl(ITokenRepo):
    def encode_jwt(
        self,
        payload: dict,
        private_key: str = settings.auth.private_key.read_text(),
        algorithm: str = settings.auth.algorithm,
        expire_timedelta: timedelta | None = None,
        expire_minutes: int = settings.auth.access_token_expire_minutes,
    ):
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)

        return encoded

    def decode_jwt(
        self,
        token: str,
        public_key: str = settings.auth.public_key.read_text(),
        algorithm: str = settings.auth.algorithm,
    ):
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])
        return decoded

    def create_token(
        self,
        token_type: str,
        token_data: dict,
        expire_minutes: int = settings.auth.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
    ):
        jwt_payload = {TokenTypeFields.TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return self.encode_jwt(
            payload=jwt_payload,
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta,
        )
