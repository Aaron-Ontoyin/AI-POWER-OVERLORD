import hashlib
from typing import Literal

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from dotenv import load_dotenv

load_dotenv(override=True)


def hash_key(key: str) -> str:
    """Hash the key using SHA-256."""
    return hashlib.sha256(key.encode()).hexdigest()


class Settings(BaseSettings):
    """Class to store all the settings of the application."""

    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    ADMIN_KEY: str
    API_KEY: str
    SECRET_KEY: str
    SESSION_TYPE: str
    SESSION_PERMANENT: bool = False
    REDIS_URL: str
    APOSTGRES_DATABASE_URL: str = (
        "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    GEMINI_API_KEY: str = ""

    FROM_EMAIL: str = "aarononto909@gmail.com"

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def customise_sources(
        cls,
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customise the settings sources order.

        Order: dotenv, file secrets, environment variables, then initialization.
        """
        return (
            dotenv_settings,
            file_secret_settings,
            env_settings,
            init_settings,
        )


settings = Settings()
