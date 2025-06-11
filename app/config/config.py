from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    database_url: str = "sqlite:///database/biblioteca.db"
    log_level: str = "INFO"
    log_file: str = "logs/api.log"


settings = Settings()
