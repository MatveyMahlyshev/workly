from abc import ABC, abstractmethod
from datetime import timedelta


class ITokenRepository(ABC):
    @abstractmethod
    def create_token(self, token_data: dict, token_type: str) -> str:
        pass

    @abstractmethod
    def encode_jwt(
        self,
        payload: dict,
        private_key: str,
        algorithm: str,
        expire_timedelta: timedelta | None,
        expire_minutes: int,
    ):
        pass

    @abstractmethod
    def decode_jwt(
        self,
        token: str,
        public_key: str,
        algorithm: str,
    ):
        pass
