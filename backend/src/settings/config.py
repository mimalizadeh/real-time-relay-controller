import os
from urllib.parse import quote_plus

from aiomqtt import Will
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    DEVICE_NAME :str = os.getenv("DEVICE_NAME", "iot_controller")

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    MQTT_HOST: str = os.getenv("MQTT_HOST", "localhost")
    MQTT_USERNAME: str = os.getenv("MQTT_USERNAME", "admin")
    MQTT_PASSWORD: str = os.getenv("MQTT_PASSWORD", "admin")
    MQTT_PORT: int = os.getenv("MQTT_PORT", 1883)
    MQTT_CONSUMER_TASK_RECONNECT_INTERVAL: int = int(os.getenv("MQTT_CONSUMER_TASK_RECONNECT_INTERVAL", 5))
    MQTT_CONSUMER_MAX_CONCURRENT_TASKS: int = int(os.getenv("MQTT_CONSUMER_MAX_CONCURRENT_TASKS", 100))

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
