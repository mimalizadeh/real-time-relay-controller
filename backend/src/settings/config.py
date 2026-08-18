import os
from urllib.parse import quote_plus

from aiomqtt import Will
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    MQTT_CLIENT_ID :str = os.getenv("MQTT_CLIENT_ID", "default_backend_node")

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    MQTT_BROKER_HOST: str = os.getenv("MQTT_BROKER_HOST", "localhost")
    MQTT_BROKER_PORT: int = os.getenv("MQTT_BROKER_PORT", 1883)
    MQTT_USERNAME: str = os.getenv("MQTT_USERNAME", "admin")
    MQTT_PASSWORD: str = os.getenv("MQTT_PASSWORD", "admin")
    MQTT_CONSUMER_TASK_RECONNECT_INTERVAL: int = int(os.getenv("MQTT_CONSUMER_TASK_RECONNECT_INTERVAL", 5))
    MQTT_CONSUMER_MAX_CONCURRENT_TASKS: int = int(os.getenv("MQTT_CONSUMER_MAX_CONCURRENT_TASKS", 100))
    MQTT_QUEUE_MAX_SIZE: int = int(os.getenv("MQTT_QUEUE_MAX_SIZE", 5000))

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
