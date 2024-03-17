from uuid import uuid4


class Message:
    def __init__(self, message, uuid=None):
        self.message = message
        self.uuid = str(uuid4()) if uuid is None else uuid

    def __str__(self):
        return f"{self.message}"

    def get_as_dictionary(self):
        return {"uuid": self.uuid, "message": self.message}
