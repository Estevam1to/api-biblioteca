from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DATABASE_URL: str = "sqlite:///database/biblioteca.db"
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"


settings = Settings()
