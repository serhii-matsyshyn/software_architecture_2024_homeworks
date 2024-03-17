import logging
import random

import requests

from message import Message

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class FacadeService:
    def __init__(self, messages_service_url="http://localhost:8002"):
        self.messages_service_url = messages_service_url

        self.logging_services = [
            "http://localhost:8003",
            "http://localhost:8004",
            "http://localhost:8005"
        ]

        self.messages_service_url = [
            "http://localhost:8001",
            "http://localhost:8002"
        ]

    def add_message(self, message_text: str):
        message = Message(message=message_text)

        logging_service_url = random.choice(self.logging_services)  # get random client

        response = requests.post(
            f"{logging_service_url}/log_message",
            json=message.get_as_dictionary()
        )
        response.raise_for_status()

        return True

    def messages(self):
        logging_service_url = random.choice(self.logging_services)
        messages_service_url = random.choice(self.messages_service_url)

        logging_response = requests.get(f"{logging_service_url}/get_all_messages")
        messages_response = requests.get(f"{messages_service_url}/messages_get_message")
        logging_response.raise_for_status()
        messages_response.raise_for_status()
        logger.debug("Get messages successful!")

        return f"{logging_response.json()} - {messages_response.json()}"
