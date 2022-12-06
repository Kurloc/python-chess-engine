from enum import Enum


class WinConditions(Enum):
    MATE = 0
    CHECKMATE = 1
    STALEMATE = 2
    RESIGNATION = 3
    TIME_OUT = 4
    KING_CAPTURED = 5
