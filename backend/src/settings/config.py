import os
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    MQTT_BROKER_URL: str = os.getenv("REDIS_HOST", "localhost")
    MQTT_USERNAME: str = os.getenv("REDIS_HOST", "admin")
    MQTT_PASSWORD: str = os.getenv("REDIS_HOST", "admin")
    MQTT_PORT: int = os.getenv("REDIS_HOST", 1883)

    DATABASE_USER: str = os.getenv("DATABASE_USER", "user")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "password")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_DB: str = os.getenv("DATABASE_DB", "iot_controller.db")

    @property
    def DATABASE_URL(self) -> str:
        """
        Construct the database URL from other settings, with the password URL-encoded.
        """
        return (
            f"sqlite+aiosqlite:///{self.DATABASE_DB}"
        )

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"


settings = Settings()
