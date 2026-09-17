from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    database_url: str
    docs_path: Path
    docs_root: Path
    docs_base_url: str = "https://fastapi.tiangolo.com/tutorial/"
    # Below this, retrieval returned nothing relevant (I observed: hits 0.50-0.65, misses 0.30-0.34)
    similarity_threshold: float = 0.4
    

settings = Settings()