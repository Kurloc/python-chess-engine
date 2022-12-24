import enum
from dataclasses import dataclass


class ChessMessageType(enum.Enum):
    BASE = 0
    MOVE = 1
    CLIENT_PLAYER_JOIN_HOST_LOBBY = 2
    CLIENT_PLAYER_JOIN_LOBBY = 3
    PLAYER_TURN_STARTED = 4
    INVALID_PLAYER_MOVE = 5
    INPUT_INPUT_PIECE_CAN_BE_UPGRADED = 6
    OUTPUT_INPUT_PIECE_CAN_BE_UPGRADED = 7
    CHAT_MESSAGE = 8

@dataclass
class ChatMessage:
    msg: str
    player_name: str

    def __init__(self, player_name: str, msg: str = ''):
        self.player_name = player_name
        self.msg = msg

    def to_dict(self):
        pass

    def from_dict(self):
        pass

    def __str__(self):
        return f'{self.player_name}: {self.msg}'

