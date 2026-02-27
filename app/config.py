from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite+aiosqlite:///./xray.db"
    secret_key: str = "dev-secret-key"
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB


settings = Settings()
