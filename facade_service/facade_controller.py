import logging
from fastapi import FastAPI

from facade_service import FacadeService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
facade_service = FacadeService()


@app.post("/facade_post_message")
async def post_message(msg: dict):
    facade_service.add_message(message_text=msg["message"])
    return {"status": "Success"}


@app.get("/facade_get_messages")
async def get_messages():
    return {"message": facade_service.messages()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
