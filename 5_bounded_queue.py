import logging
import time
from multiprocessing import Process, Value

import hazelcast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def producer():
    time.sleep(1)  # Wait for consumers to start
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue").blocking()

    for i in range(100):
        value = "value-" + str(i)
        # Offer the value to the queue, blocking if the queue is full
        queue.offer(value)  # put or offer
        logger.info("Producing {}".format(value))

    # Shutdown the Hazelcast client
    client.shutdown()


def consumer(consumer_id, items_consumed):
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue").blocking()

    while not items_consumed.value:
        # Poll the queue with a timeout to avoid blocking indefinitely
        head = queue.poll(5)
        if head:
            logger.info("Consumer {}: Consuming {}".format(consumer_id, head))

    # Shutdown the Hazelcast client
    client.shutdown()


if __name__ == "__main__":
    # Create a shared variable to track if all items have been consumed
    items_consumed = Value("i", 0)

    # Start one producer and two consumers simultaneously as separate processes
    producer_process = Process(target=producer)
    consumer_process_1 = Process(target=consumer, args=(1, items_consumed))
    consumer_process_2 = Process(target=consumer, args=(2, items_consumed))

    producer_process.start()
    consumer_process_1.start()
    consumer_process_2.start()

    # Wait for the producer to finish
    producer_process.join()

    # Set the flag to indicate that all items have been produced
    with items_consumed.get_lock():
        items_consumed.value = 1

    # Wait for the consumers to finish
    consumer_process_1.join()
    consumer_process_2.join()
