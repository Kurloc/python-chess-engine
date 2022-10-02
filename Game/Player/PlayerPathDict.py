from typing import Dict, Tuple

from Game.Pieces.IPiece import IPiece
from Pathfinding.PathfindingTile import PathFindingTile
from Pathfinding.Vector2 import Vector2


class PlayerPathDict:
    piece: IPiece
    position: Vector2
    paths: Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]]

    def __init__(self,
                 path_dict: Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]],
                 piece: IPiece,
                 position: Vector2):
        self.paths = path_dict
        self.piece = piece
        self.position = position
