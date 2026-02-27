from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()
import os


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PW: str

    class Config:
        env_file = ".env"


settings = Settings()
