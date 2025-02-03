from typing import List
from pydantic import validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    # Definimos allowed_origins como una lista de strings con un valor por defecto para desarrollo.
    allowed_origins: List[str] = ["http://localhost:5173"]

    @validator("allowed_origins", pre=True)
    def split_allowed_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",")]
        return value

    class Config:
        env_file = ".env"  # Archivo que contiene las variables de entorno

settings = Settings()