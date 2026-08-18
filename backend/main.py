import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure.mqtt.producer import get_mqtt_producer
from src.settings.config import settings
from src.settings.logging_config import setup_logging
from src.routes import relay

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    logger.info("Application startup...")

    # Start MQTT producer
    producer = get_mqtt_producer()
    await producer.start()
    logger.info("MQTT producer started.")
    yield

    # Shutdown event
    logger.info("Application shutdown.")
    # Stop MQTT producer
    await producer.stop()
    logger.info("MQTT producer stopped.")


app = FastAPI(
    title="Real time relay controller",
    description="Real time relay controller",
    lifespan=lifespan
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(relay.router)
