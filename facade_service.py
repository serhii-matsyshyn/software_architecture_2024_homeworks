import logging
from uuid import uuid4

import requests
from fastapi import FastAPI

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

logging_service_url = "http://localhost:8001"
messages_service_url = "http://localhost:8002"
messages = {}


@app.post("/facade_post_message")
async def post_message(msg: dict):
    response = requests.post(
        f"{logging_service_url}/log_message",
        json={"uuid": str(uuid4()), "message": msg["message"]}
    )
    response.raise_for_status()
    return {"status": "Success"}


@app.get("/facade_get_messages")
async def get_messages():
    logging_response = requests.get(f"{logging_service_url}/get_all_messages")
    messages_response = requests.get(f"{messages_service_url}/messages_get_message")
    logging_response.raise_for_status()
    messages_response.raise_for_status()
    logger.debug("Get messages successful!")
    return {
        "message": f"{logging_response.json()} - {messages_response.json()['message']}"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
