import asyncio
import logging
import aiomqtt
import json

from src.infrastructure.mqtt.base import MqttInfrastructure

logger = logging.getLogger(__name__)

from src.settings.config import settings


class MessageProducer(MqttInfrastructure):

    def __init__(self, client_id: str, clean_session: bool = False):

        self.client_id = f"{client_id}_producer"
        super().__init__(client_id=client_id, clean_session=clean_session)
        self._outbound_queue: asyncio.Queue[tuple[str, bytes, int]] = asyncio.Queue(maxsize=5000)
        self._is_running = False
        self._publish_task: asyncio.Task | None = None

    async def start(self) -> None:
        self._is_running = True
        self._publish_task = asyncio.create_task(self._publish_loop())
        logger.info("Producer background task started")

    async def stop(self) -> None:
        logger.info("Stopping publisher...")
        self._is_running = False
        if self._publish_task:
            self._publish_task.cancel()
            await asyncio.gather(self._publish_task, return_exceptions=True)

    async def emit(self, topic: str, payload: dict | bytes, qos: int = 1) -> None:
        if isinstance(payload, dict):
            payload = json.dumps(payload).encode("utf-8")

        try:
            await asyncio.wait_for(
                self._outbound_queue.put((topic, payload, qos)),
                timeout=1.0
            )
        except asyncio.TimeoutError:
            logger.critical(f"Outbound queue full! Dropping outgoing message to {topic}")
            raise Exception("System overloaded, cannot publish message")

    async def _publish_loop(self) -> None:
        base_interval = settings.MQTT_CONSUMER_TASK_RECONNECT_INTERVAL
        reconnect_interval = base_interval

        while self._is_running:
            try:
                async with self._client:
                    reconnect_interval = base_interval  # Reset on success
                    logger.info("Producer connected to Broker.")

                    while self._is_running:
                        topic, payload, qos = await self._outbound_queue.get()
                        try:
                            await self._client.publish(topic, payload=payload, qos=qos)
                        except Exception as e:
                            logger.error(f"Failed to publish to {topic}: {e}")
                            # await self._outbound_queue.put((topic, payload, qos))
                            raise e
                        finally:
                            self._outbound_queue.task_done()

            except aiomqtt.MqttError as error:
                if not self._is_running:
                    break
                logger.warning(f"Producer connection lost: {error}. Reconnecting in {reconnect_interval}s...")
                await asyncio.sleep(reconnect_interval)
                reconnect_interval = min(reconnect_interval * 2, 60)

# Global producer instance
mqtt_producer = MessageProducer(client_id=settings.MQTT_CLIENT_ID)

def get_mqtt_producer()-> MessageProducer:
    return mqtt_producer