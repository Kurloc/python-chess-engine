import json
from dataclasses import dataclass
from typing import List

from ChessEngine.Board.BoardEventPiece import BoardEventPiece
from ChessEngine.Board.BoardEventTypes import BoardEventTypes
from ChessEngine.Pathfinding.Vector2 import Vector2


@dataclass
class BoardEvent:
    event_type: BoardEventTypes
    pieces_involved: List[BoardEventPiece]
    turn_index: int
    move_to_position: Vector2

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda x: x.__dict__)