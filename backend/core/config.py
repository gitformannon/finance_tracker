from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    TELEGRAM_BOT_TOKEN: str
    WEBHOOK_URL: str
    PORT: int
    SEED_ENABLED: bool
    BACKEND_URL:str

    class Config:
        env_file = ".env"

settings = Settings()