import asyncio
import logging

from src.infrastructure.mqtt.consumer import MessageConsumer
from src.settings.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting consumer...")

    consumer = MessageConsumer(clean_session=True)
    try:

        # Start consuming messages
        await consumer.consume("devices/+/+/status")

    finally:
        await consumer.stop()
        logger.info("Stop consumer...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Consumer stopped by user.")
