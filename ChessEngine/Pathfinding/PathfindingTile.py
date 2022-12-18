import dataclasses
from typing import Dict, cast, Tuple

from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.PieceDeserializer import PieceDeserializer
from ChessEngine.Pydantic.TupleToString import tuple_to_string, string_to_tuple


@dataclasses.dataclass
class PathFindingTile:
    position: Vector2
    move_can_be_used_as_an_attack: bool = False
    is_blocked: bool = False
    is_enemy: bool = False
    is_attack_only: bool = False
    piece: IPiece = None

    def __init__(self,
                 move_can_be_used_as_an_attack: bool,
                 is_blocked: bool,
                 is_enemy: bool,
                 is_attack_move: bool,
                 position_of_tile: Vector2,
                 piece_on_tile: IPiece = None):
        self.move_can_be_used_as_an_attack = move_can_be_used_as_an_attack
        self.is_blocked = is_blocked
        self.is_enemy = is_enemy
        self.is_attack_only = is_attack_move
        self.position = position_of_tile
        self.piece = piece_on_tile

    def to_dict(self):
        return {
            'position': tuple_to_string(self.position.get_tuple()),
            'move_can_be_used_as_an_attack': self.move_can_be_used_as_an_attack,
            'is_blocked': self.is_blocked,
            'is_enemy': self.is_enemy,
            'is_attack_only': self.is_attack_only,
            'piece': None if self.piece is None else self.piece.to_dict()
        }

    @staticmethod
    def from_dict(value: Dict):
        piece_Value = value.get('piece')
        return PathFindingTile(
            move_can_be_used_as_an_attack=value['move_can_be_used_as_an_attack'],
            is_blocked=value['is_blocked'],
            is_enemy=value['is_enemy'],
            is_attack_move=value['is_attack_only'],
            position_of_tile=Vector2.from_tuple(cast(Tuple[int, int], string_to_tuple(value['position']))),
            piece_on_tile=None if piece_Value is None else PieceDeserializer.from_dict(piece_Value)
        )
