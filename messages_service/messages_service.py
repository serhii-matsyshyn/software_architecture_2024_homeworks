import logging
from threading import Thread

import hazelcast

from message import Message

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MessagesService:
    def __init__(self):
        self.internal_memory_storage = []

        self.client = hazelcast.HazelcastClient(cluster_name="dev")

        self.distributed_queue = self.client.get_queue("queue").blocking()
        self.running = True

        self.consumer = Thread(target=self.consume_messages)
        self.consumer.start()

    def get_stored_messages(self):
        return [msg.message for msg in self.internal_memory_storage]

    def consume_messages(self):
        while self.running:
            data = self.distributed_queue.poll(3)
            if data:
                logger.info(f"Consuming {data}")
                self.internal_memory_storage.append(Message(data))

    def __del__(self):
        self.running = False
        self.consumer.join()
