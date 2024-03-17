import atexit
import logging
import os
import signal
import subprocess
import time

import hazelcast

from message import Message

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LoggingService:
    def __init__(self, hazelcast_path):
        os.chdir(hazelcast_path)
        self.process = subprocess.Popen(
            "hz-start.bat", cwd=hazelcast_path,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )

        # Registering a cleanup function to terminate the process on program exit
        atexit.register(self._cleanup)

        time.sleep(10)

        self.client = hazelcast.HazelcastClient(cluster_name="dev")

        self.distributed_map = self.client.get_map("map").blocking()
        self.distributed_queue = self.client.get_queue("queue").blocking()

    def _cleanup(self):
        logger.info("Terminating hazelcast")
        try:
            # Terminate the subprocess
            self.process.terminate()
            time.sleep(2)

            # Check if the process is still running and force termination if necessary
            if self.process.poll() is None:
                os.kill(self.process.pid, signal.SIGTERM)
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")

    def add_message(self, message: Message):
        logger.info(f"Logged message: {message}")
        self.distributed_map.put(message.uuid, message.message)
        self.distributed_queue.offer(message.message, timeout=5)

    def get_messages(self):
        return [val for val in self.distributed_map.values()]
