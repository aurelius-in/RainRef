from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pydantic import field_validator
import json


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, case_sensitive=False, env_prefix="")
    api_key: str | None = None
    allowed_origins: List[str] | str = ["http://localhost:5173"]
    log_level: str = "INFO"
    cors_allow_credentials: bool = False

    # App info
    app_version: str = "0.1.0"
    git_sha: str = "dev"

    # Rate limiting for actions
    rate_limit_window_sec: int = 60
    rate_limit_per_window: int = 10
    redis_url: str | None = None
    use_redis_limiter: bool = False

    # Auth / JWT
    require_jwt_for_admin: bool = False
    # allow override via env var REQUIRE_JWT_FOR_ADMIN
    jwt_secret: str = "change-me-dev"
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 60

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def _coerce_origins(cls, v):
        if isinstance(v, str):
            s = v.strip()
            try:
                loaded = json.loads(s)
                if isinstance(loaded, list):
                    return [str(it).strip() for it in loaded]
            except Exception:
                pass
            s = s.strip(' []')
            return [p.strip().strip('"\'') for p in s.split(',') if p.strip()]
        return v


settings = Settings()

