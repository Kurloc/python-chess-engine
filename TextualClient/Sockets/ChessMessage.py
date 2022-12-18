import abc
from typing import Any

import pydantic
from pydantic import BaseModel

from ChessEngine.Pydantic.ArbitraryConfig import Config
from TextualClient.Sockets.ChessMessageType import ChessMessageType


@pydantic.dataclasses.dataclass(config=Config)
class ChessMessage(BaseModel, abc.ABC):
    message_type: ChessMessageType
    message_value: str

    def __init__(
            self,
            message_type: ChessMessageType,
            message_value: str,
            **data: Any
    ):
        super().__init__(message_type=message_type, message_value=message_value, **data)
