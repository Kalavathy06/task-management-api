from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MacV AI Task API"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    DATABASE_URL: str
    REDIS_URL: str = "redis://redis:6379/0"

    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str | None
    SMTP_PASSWORD: str | None
    EMAIL_FROM: str

    class Config:
        env_file = ".env"

settings = Settings()