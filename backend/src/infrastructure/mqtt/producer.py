import logging

from aiomqtt import Client, MqttError
from src.infrastructure.mqtt.base import MqttInfrastructure

logger = logging.getLogger(__name__)


class MessageProducer(MqttInfrastructure):

    def __init__(self, client_id: str | None = None, clean_session: bool = False):
        self.client_id = client_id
        super().__init__(client_id=self.client_id, clean_session=clean_session)


def get_message_producer(client_id: str | None = None, clean_session: bool = False) -> MessageProducer:
    return MessageProducer(client_id, clean_session)
