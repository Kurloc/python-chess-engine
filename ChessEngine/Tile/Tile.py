from dataclasses import dataclass
from typing import Union

import pydantic
from pydantic import BaseModel

from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pydantic.ArbitraryConfig import Config
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
