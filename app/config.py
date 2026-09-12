from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    database_url: str
    docs_path: Path

settings = Settings()