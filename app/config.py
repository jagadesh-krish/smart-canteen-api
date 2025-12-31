from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://canteen_user:canteen_password@localhost:5432/smart_canteen_db"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
