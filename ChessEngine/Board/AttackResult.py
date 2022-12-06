from typing import List
from ChessEngine.Board.BoardEventTypes import BoardEventTypes
from ChessEngine.Board.BoardEventPiece import BoardEventPiece

class AttackResult:
    success: bool = False
    board_event_type: BoardEventTypes
    pieces_involved: List[BoardEventPiece]

    def __init__(self,
                 success: bool,
                 board_event_type: BoardEventTypes,
                 pieces_involved: List[BoardEventPiece] = None):
        if pieces_involved is None:
            pieces_involved = []

        self.success = success
        self.board_event_type = board_event_type
        self.pieces_involved = pieces_involved
