from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./biblioteca.db"
    log_level: str = "INFO"
    log_file: str = "logs/api.log"

    class Config:
        env_file = ".env"


settings = Settings()
