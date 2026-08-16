import asyncio
import json
import logging
from typing import Any, Literal
from aiomqtt import Client, MqttError, Will
from pydantic import BaseModel, ValidationError

from src.settings.config import settings

logger = logging.getLogger(__name__)


class MqttInfrastructure:

    def __init__(self, client_id: str | None, clean_session: bool = False):
        self.client_id = client_id
        self.topic = f"devices/{settings.DEVICE_NAME}/status"
        will_message = Will(
            topic=self.topic,
            payload="offline",
            qos=1,
            retain=True
        )

        self._client = Client(
            hostname=settings.MQTT_HOST,
            port=settings.MQTT_PORT,
            username=settings.MQTT_USERNAME,
            password=settings.MQTT_PASSWORD,
            clean_session=clean_session,
            identifier=self.client_id,
            will=will_message,
        )

    async def _send_live_signal(self, message: Literal["offline", "online"]):
        await self.publish(self.topic, message, retain=True)

    async def publish(self, topic: str, message: str, qos: int = 1, retain: bool = False) -> None:
        try:
            async with self._client:
                await self._client.publish(topic, payload=message, qos=qos, retain=retain)
                logger.info(f"Published to {topic}:{message}")
        except MqttError as e:
            logger.error(f"failed to publish to MQTT broker: {e}")
