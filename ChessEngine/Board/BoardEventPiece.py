from dataclasses import dataclass
from typing import Union

from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.IPiece import IPiece


@dataclass
class BoardEventPiece:
    piece: IPiece
    starting_position: [Vector2, None]
    ending_position: Union[Vector2, None]

    def __init__(self, piece: IPiece,
                 starting_position: Union[Vector2, None] = None,
                 ending_position: Union[Vector2, None] = None):
        self.piece = piece
        self.starting_position = starting_position
        self.ending_position = ending_position