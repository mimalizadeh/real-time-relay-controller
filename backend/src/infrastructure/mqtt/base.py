
import logging
from typing import Literal, Callable, Awaitable
from aiomqtt import Client, MqttError, Will

from src.settings.config import settings

logger = logging.getLogger(__name__)

MessageHandler = Callable[[str, bytes], Awaitable[None]]


class MqttInfrastructure:

    def __init__(self, client_id: str | None, clean_session: bool = False):
        self.client_id = client_id or settings.MQTT_CLIENT_ID
        self.topic = f"system/nodes/{self.client_id}/status"

        will = Will(
            topic=self.topic,
            payload="offline_unexpectedly",
            qos=1,
            retain=True
        )

        self._client = Client(
            hostname=settings.MQTT_BROKER_HOST,
            port=settings.MQTT_BROKER_PORT,
            username=settings.MQTT_USERNAME,
            password=settings.MQTT_PASSWORD,
            identifier=self.client_id,
            clean_session=clean_session,
            will=will
        )

    async def _send_live_signal(self, status: Literal["offline", "online"]):
        try:
            await self._client.publish(self.topic, payload=status, qos=1, retain=True)
            logger.info(f"Node status updated to: {status}")
        except MqttError as error:
            logger.error(f"Failed to send live signal: {error}")
