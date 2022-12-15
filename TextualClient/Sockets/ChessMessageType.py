import enum


class ChessMessageType(enum.Enum):
    BASE = 0
    MOVE = 1
    PLAYER_TURN_STARTED = 2


