import argparse
import logging
from typing import Dict

from fastapi import FastAPI

from logging_service import LoggingService
from message import Message

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()

logging_service = LoggingService(hazelcast_path=r"D:\STUDY_2023-2024_2\software_architecture\software_architecture_2024_homeworks_2\hazelcast\hazelcast-5.3.6\bin")


@app.post("/log_message")
async def log_message(msg: Dict[str, str]):
    logging_service.add_message(Message(**msg))
    return {"status": "Message logged successfully"}


@app.get("/get_all_messages")
async def get_all_messages():
    return logging_service.get_messages()


if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="Specify the port number", required=True)
    args = parser.parse_args()

    uvicorn.run(app, host="0.0.0.0", port=args.port)
