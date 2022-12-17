from dataclasses import dataclass
from typing import Union, Dict, cast, Tuple

from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pieces.PieceDeserializer import PieceDeserializer
from ChessEngine.Pydantic.TupleToString import tuple_to_string, string_to_tuple


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

    @staticmethod
    def from_dict(incoming_value: Dict):
        return BoardEventPiece(
            PieceDeserializer.from_dict(incoming_value.get('piece')),
            (
                None if len(incoming_value.get('starting_position', '').strip()) == 0
                else Vector2.from_tuple(cast(Tuple[int, int], string_to_tuple(incoming_value.get('starting_position'))))
            ),
            (
                None if len(incoming_value.get('ending_position', '').strip()) == 0
                else Vector2.from_tuple(cast(Tuple[int, int], string_to_tuple(incoming_value.get('ending_position'))))
            )
        )

    def to_dict(self):
        return {
            'piece': self.piece.to_dict(),
            'starting_position': (
                None if self.starting_position is None
                else tuple_to_string(self.starting_position.get_tuple())
            ),
            'ending_position': (
                None if self.ending_position is None
                else tuple_to_string(self.ending_position.get_tuple())
            )
        }
