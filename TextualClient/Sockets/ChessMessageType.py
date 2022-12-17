import enum


class ChessMessageType(enum.Enum):
    BASE = 0
    MOVE = 1
    PLAYER_TURN_STARTED = 2
    INVALID_PLAYER_MOVE = 3
    INPUT_INPUT_PIECE_CAN_BE_UPGRADED = 4
    OUTPUT_INPUT_PIECE_CAN_BE_UPGRADED = 5


