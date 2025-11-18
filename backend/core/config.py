from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path
import os
BASE_DIR = Path(
    __file__
).parent.parent  # абсолютный адрес базовой директории для файла бд


class AuthJWT(BaseModel):
    private_key: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30


class DBSettings(BaseModel):
    url: str = os.getenv("DB_URL") or "postgresql+asyncpg://postgres:postgres@localhost:5432/workly_db"
    echo: bool = False


class Settings(BaseSettings):
    auth: AuthJWT = AuthJWT()
    db: DBSettings = DBSettings()
    api_v1_prefix: str = "/api/v1"


settings = Settings()
