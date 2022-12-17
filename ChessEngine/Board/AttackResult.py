from typing import List, Dict
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

    @staticmethod
    def from_dict(incoming_value: Dict):
        return AttackResult(
            incoming_value.get('success'),
            BoardEventTypes(incoming_value.get('board_event_type')),
            [BoardEventPiece.from_dict(piece) for piece in incoming_value.get('pieces_involved')]
        )

    def to_dict(self):
        return {
            'success': self.success,
            'board_event_type': self.board_event_type.value,
            'pieces_involved': [piece.to_dict() for piece in self.pieces_involved]
        }
