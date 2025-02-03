from typing import List
from pydantic import validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    allowed_origins: List[str] = ["http://localhost:5173"]

    @validator("allowed_origins", pre=True)
    def split_allowed_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    class Config:
        env_file = ".env"

settings = Settings()