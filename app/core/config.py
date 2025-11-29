from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30


class DBSettings(BaseModel):
    url: str = (
        os.getenv("DB_URL")
        or "postgresql+asyncpg://postgres:postgres@localhost:5432/arch_db"
    )
    echo: bool = True


class Settings(BaseSettings):
    auth: AuthJWT = AuthJWT()
    db: DBSettings = DBSettings()
    api_v1_prefix: str = "/api/v1"
    api_v2_prefix: str = "/api/v2"


settings = Settings()
