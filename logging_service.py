import logging
from typing import Dict

from fastapi import FastAPI

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
messages = {}


@app.post("/log_message")
async def log_message(msg: Dict[str, str]):
    uuid = msg["uuid"]
    message = msg["message"]
    messages[uuid] = message
    logger.debug(f"Logged message: {uuid}: {message}")
    return {"status": "Message logged successfully"}


@app.get("/get_all_messages")
async def get_all_messages():
    return list(messages.values())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
