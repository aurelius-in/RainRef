from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    allowed_origins: List[str] = ["http://localhost:5173"]
    log_level: str = "INFO"
    cors_allow_credentials: bool = False

    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = ".env"

settings = Settings()
