import argparse
import logging

from fastapi import FastAPI

from messages_service import MessagesService

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()

messages_service = MessagesService()


@app.get("/messages_get_message")
async def get_all_messages():
    return messages_service.get_stored_messages()


if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="Specify the port number", required=True)
    args = parser.parse_args()

    uvicorn.run(app, host="0.0.0.0", port=args.port)
