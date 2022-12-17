from pydantic import BaseModel
from TextualClient.Sockets.MessageTypeBase import MessageTypeBase


class Message(BaseModel):
    message_type: MessageTypeBase
    value: str

    def __init__(
            self,
            message_type: MessageTypeBase,
            value: str = ''
    ):
        super().__init__(
            message_type=message_type,
            value=value
        )
