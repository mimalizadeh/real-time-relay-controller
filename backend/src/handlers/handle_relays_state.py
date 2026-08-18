import json
import logging

logger = logging.getLogger(__name__)


async def handle_relay_state_change(topic: str, payload: bytes | str) -> None:
    """
     Topic: devices/+/state/relay/+
    """
    try:
        parts = topic.split("/")
        device_id = parts[1]
        relay_id = int(parts[4])
        physical_state = payload

        if isinstance(payload, bytes):
            data = json.loads(payload.decode("utf-8"))
        else:
            data = json.loads(payload)

        physical_state = data.get("action").upper()
        if physical_state not in ("ON", "OFF"):
            raise ValueError(f"Invalid hardware state: {physical_state}")

        logger.info(f"Hardware confirmation received: {device_id} Relay {relay_id} is physically {physical_state}")

    except Exception as e:
        logger.error(f"Failed to process hardware state update from {topic}: {e}")
