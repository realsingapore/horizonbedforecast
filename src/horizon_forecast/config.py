from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    APP_ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()