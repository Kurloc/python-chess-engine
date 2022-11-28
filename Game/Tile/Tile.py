from typing import Union

from Game.Pieces.IPiece import IPiece
from Game.Tile.TileColors import TileColors
from Game.Pathfinding.Vector2 import Vector2

class Tile:
    tile_color: TileColors
    piece: Union[IPiece, None]
    position: Vector2

    def __init__(self, position: Vector2, tile_color: TileColors, piece: IPiece = None):
        self.position = position
        self.tile_color = tile_color
        self.piece = piece
