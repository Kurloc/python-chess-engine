import enum


class ChessMessageType(enum.Enum):
    BASE = 0
    MOVE = 1
    PLAYER_JOIN_LOBBY = 2
    PLAYER_TURN_STARTED = 3
    INVALID_PLAYER_MOVE = 4
    INPUT_INPUT_PIECE_CAN_BE_UPGRADED = 5
    OUTPUT_INPUT_PIECE_CAN_BE_UPGRADED = 6


