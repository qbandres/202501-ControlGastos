from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    # Definimos allowed_origins como un string
    allowed_origins: List[str]=[]


    class Config:
        env_file = ".env"  # Archivo que contiene las variables de entorno

settings = Settings()