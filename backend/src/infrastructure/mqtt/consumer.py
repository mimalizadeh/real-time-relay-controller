import asyncio
import logging
from typing import Any

from aiomqtt import MqttError, Message
from pydantic import ValidationError

from src.settings.config import settings
from src.infrastructure.mqtt.base import MqttInfrastructure

logger = logging.getLogger(__name__)


class MessageConsumer(MqttInfrastructure):

    def __init__(self, client_id: str | None = None, clean_session: bool = False):
        self.client_id = client_id
        super().__init__(client_id=self.client_id, clean_session=clean_session)

    @staticmethod
    async def _process_message(message: Message) -> None:
        try:
            payload = message.payload.decode()
            logger.info(f"{message.topic} : {payload}")
        except ValidationError as e:
            logger.error(f"Invalid message format dropped: {e}")
        except Exception as e:
            logger.error(f"Failed to process message: {e}")

    async def stop(self):
        try:
            await self._send_live_signal("offline")
            await self._client.unsubscribe()
        except MqttError as error:
            logger.error(f"MQTT connection lost: {error}")

    async def consume(self, topic: str, qos: int = 1) -> None:
        semaphore = asyncio.Semaphore(settings.MQTT_CONSUMER_MAX_CONCURRENT_TASKS)
        reconnect_interval = settings.MQTT_CONSUMER_TASK_RECONNECT_INTERVAL

        await self._send_live_signal("online")

        async def _bounded_process(msg: Any):
            async with semaphore:
                await self._process_message(msg)

        while True:
            try:
                async with self._client:
                    await self._client.subscribe(topic, qos=qos)
                    logger.info(f"Subscribed to {topic} with QoS {qos}")
                    async for message in self._client.messages:
                        asyncio.create_task(_bounded_process(message))

            except MqttError as error:
                logger.warning(f"MQTT connection lost: {error}. Reconnecting in {reconnect_interval}s...")
                await asyncio.sleep(reconnect_interval)
                reconnect_interval = min(reconnect_interval * 2, 60)  # Exponential backoff
