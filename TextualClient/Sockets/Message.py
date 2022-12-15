import uuid
from typing import Any

from pydantic import BaseModel

from TextualClient.Sockets.MessageTypeBase import MessageTypeBase


class Message(BaseModel):
    message_type: MessageTypeBase
    packet_number: int = 1
    packet_total: int = 1
    message_id: str
    value: str

    def __init__(
            self,
            message_type: MessageTypeBase,
            packet_number: int = 1,
            packet_total: int = 1,
            message_id: str = str(uuid.uuid4()),
            value: str = ''
    ):
        super().__init__(
            message_type=message_type,
            packet_number=packet_number,
            packet_total=packet_total,
            message_id=message_id,
            value=value
        )
