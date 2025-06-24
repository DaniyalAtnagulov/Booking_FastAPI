from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


# В версии Pydantic 2.0 модуль BaseSettings был вынесен в отдельную библиотеку pydantic-settings.
# Необходимо установить её через: pip install pydantic-settings

class Settings(BaseSettings):
    # Основные настройки
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Настройки основной базы данных
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # Настройки тестовой базы данных
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def DATABASE_TEST_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}"
            f"@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )

    # Настройки SMTP
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    # Безопасность
    SECRET_KEY: str
    ALGORITHM: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int

    # Указание .env файла
    model_config = SettingsConfigDict(env_file=".env")


# Создание экземпляра настроек
settings = Settings()