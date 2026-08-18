import json
import logging
from typing import Any, Literal

from fastapi.params import Depends

from src.infrastructure.mqtt.producer import MessageProducer, get_mqtt_producer

logger = logging.getLogger(__name__)
from datetime import datetime, timezone


class RelayControlService:
    def __init__(self, producer: MessageProducer):
        self.producer = producer

    async def request_relay_change_state(self, device_id: str, relay_id: int, state: Literal["on", "off"]) -> None:
        """
        This method call from API (example : FastAPI)
        we only send 'request' . don't update database here
        """
        topic = f"devices/{device_id}/commands/relay/{relay_id}"
        payload = {"action": state, "timestamp": self._get_utc_now()}

        await self.producer.emit(topic=topic, payload=payload, qos=1)

        logger.info(f"Command dispatched to {topic}. Waiting for physical confirmation.")

    @staticmethod
    def _get_utc_now() -> str:
        return datetime.now(timezone.utc).isoformat()


def get_relay_control_service(producer: MessageProducer = Depends(get_mqtt_producer)) -> RelayControlService:
    return RelayControlService(producer)
