import asyncio
import json
import logging
from typing import Any
from aiomqtt import Client, MqttError
from pydantic import BaseModel, ValidationError

from src.settings.config import settings

logger = logging.getLogger(__name__)


class MqttInfrastructure:
    def __init__(self, client_id: str = "", clean_session: bool = False):
        self.client_id = client_id

        self._client = Client(
            hostname=settings.MQTT_HOST,
            port=settings.MQTT_PORT,
            username=settings.MQTT_USERNAME,
            password=settings.MQTT_PASSWORD,
            clean_session=clean_session,
            identifier=self.client_id
        )

    async def publish_signal(self, topic: str, payload: str, qos: int = 1) -> None:
        logger.info(f"Publishing to MQTT broker: {payload}")
        try:
            async with self._client:
                await self._client.publish(topic, payload=payload, qos=qos)
                logger.info(f"Published to {topic}: {payload}")
        except MqttError as e:
            logger.error(f"Failed to publish to MQTT broker: {e}")
            raise

    async def start_subscriber(self, topic: str, qos: int = 1) -> None:
        reconnect_interval = 3

        max_concurrent_tasks = 100
        semaphore = asyncio.Semaphore(max_concurrent_tasks)

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
