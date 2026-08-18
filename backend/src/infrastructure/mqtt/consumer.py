import asyncio
import logging
from typing import Sequence
import aiomqtt

from src.infrastructure.mqtt.base import MqttInfrastructure
from src.settings.config import settings

logger = logging.getLogger(__name__)


class MessageConsumer(MqttInfrastructure):
    def __init__(
            self,
            shared_queue: asyncio.Queue,
            client_id: str | None = None,
            clean_session: bool = False
    ):
        super().__init__(client_id=client_id, clean_session=clean_session)
        self._queue = shared_queue
        self._active_topics: list[tuple[str, int]] = []
        self._is_running = False

    async def consume(self, topics: Sequence[tuple[str, int]]) -> None:
        self._active_topics = list(topics)
        self._is_running = True
        base_reconnect_interval = settings.MQTT_CONSUMER_TASK_RECONNECT_INTERVAL
        current_interval = base_reconnect_interval

        while self._is_running:
            try:
                async with self._client:
                    current_interval = base_reconnect_interval
                    await self._send_live_signal("online")

                    for topic, qos in self._active_topics:
                        await self._client.subscribe(topic, qos=qos)

                    logger.info(f"Subscribed to: {[t[0] for t in self._active_topics]}")

                    async for message in self._client.messages:
                        if not self._is_running:
                            break

                        payload = message.payload.decode() if isinstance(message.payload, bytes) else str(
                            message.payload)
                        topic = str(message.topic)

                        try:
                            # Backpressure Mechanism
                            await asyncio.wait_for(
                                self._queue.put((topic, payload)),
                                timeout=2.0
                            )
                        except asyncio.TimeoutError:
                            logger.critical(f"System overloaded. Queue full. Dropped message from {topic}")

            except aiomqtt.MqttError as error:
                if not self._is_running:
                    break
                logger.warning(f"MQTT network error: {error}. Reconnecting in {current_interval}s...")
                await asyncio.sleep(current_interval)
                current_interval = min(current_interval * 2, 60)
            except Exception as e:
                logger.critical(f"Fatal consumer error: {e}", exc_info=True)
                await asyncio.sleep(5)

    async def stop(self) -> None:
        self._is_running = False
        logger.info("Stopping MQTT Consumer...")

        try:
            async with aiomqtt.Client(
                    hostname=settings.MQTT_BROKER_HOST,
                    port=settings.MQTT_BROKER_PORT,
                    username=settings.MQTT_USERNAME,
                    password=settings.MQTT_PASSWORD,
                    identifier=f"{self.client_id}_shutdown"
            ) as temp_client:
                topic = f"system/nodes/{self.client_id}/status"
                await temp_client.publish(topic, payload="offline", qos=1, retain=True)
        except Exception as e:
            logger.error(f"Failed to publish offline status during shutdown: {e}")