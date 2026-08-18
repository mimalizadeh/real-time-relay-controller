import asyncio
import logging

from src.settings.logging_config import setup_logging
from src.handlers.handle_device_lwt import handle_device_lwt
from src.handlers.handle_relays_state import handle_relay_state_change
from src.settings.config import settings
from src.infrastructure.mqtt.router import MQTTRouter, MessageDispatcher
from src.infrastructure.mqtt.consumer import MessageConsumer

setup_logging()
logger = logging.getLogger(__name__)


async def main():
    router = MQTTRouter()
    router.add_route(f"devices/+/state/relay/+", handle_relay_state_change, qos=2)
    router.add_route("devices/+/status", handle_device_lwt, qos=0)

    shared_queue = asyncio.Queue(maxsize=settings.MQTT_QUEUE_MAX_SIZE)

    dispatcher = MessageDispatcher(
        router=router,
        queue=shared_queue,
        max_workers=settings.MQTT_CONSUMER_MAX_CONCURRENT_TASKS
    )

    consumer = MessageConsumer(
        shared_queue=shared_queue,
        client_id=f"{settings.MQTT_CLIENT_ID}_consumer",
        clean_session=False
    )

    await dispatcher.start()

    consumer_task = asyncio.create_task(
        consumer.consume(router.get_subscription_topics())
    )

    try:
        await consumer_task
    except asyncio.CancelledError:
        logger.info("Shutdown signal received. Initiating graceful shutdown...")
    finally:
        await consumer.stop()

        logger.info("Draining internal message queue to prevent data loss...")
        await dispatcher.stop()
        logger.info("Shutdown complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass