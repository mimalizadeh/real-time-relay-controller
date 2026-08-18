import json
import logging

logger = logging.getLogger(__name__)


async def handle_device_lwt(topic: str, payload: bytes | str) -> None:
    """
     Topic: devices/+/status
    """
    device_id = topic.split("/")[1]
    if isinstance(payload, bytes):
        status = payload.decode("utf-8")  # "online" or "offline"
    else:
        status = payload

    if status == "offline":
        logger.critical(f"CRITICAL: Edge device {device_id} dropped off the network! (LWT triggered)")
