from dataclasses import dataclass
from typing import Union, Dict, cast, Tuple

import pydantic
from pydantic import BaseModel

from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pieces.PieceDeserializer import PieceDeserializer
from ChessEngine.Pydantic.ArbitraryConfig import Config
from ChessEngine.Pydantic.TupleToString import tuple_to_string, string_to_tuple
from ChessEngine.Tile.TileColors import TileColors
from ChessEngine.Pathfinding.Vector2 import Vector2


class Tile(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

    piece: Union[IPiece, None]
    position: Vector2
    tile_color: TileColors

    def __init__(self, position: Vector2, tile_color: TileColors, piece: IPiece = None):
        super().__init__(position=position, tile_color=tile_color, piece=piece)
        self.position = position
        self.tile_color = tile_color
        self.piece = piece

    def to_dict(self):
        return {
            'piece': self.piece.to_dict(),
            'position': tuple_to_string(self.position.get_tuple()),
            'tile_color': self.tile_color.value
        }

    @staticmethod
    def from_dict(incoming_value: Dict):
        return Tile(
            Vector2.from_tuple(cast(Tuple[int, int], string_to_tuple(incoming_value.get('position')))),
            TileColors(incoming_value.get('tile_color')),
            PieceDeserializer.from_dict(incoming_value.get('piece'))
        )
