from typing import Dict, Tuple

from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pathfinding.PathfindingTile import PathFindingTile
from ChessEngine.Pathfinding.Vector2 import Vector2


class PlayerPathDict:
    piece: IPiece
    position: Vector2
    paths: Dict[Tuple[Tuple[int, int], Tuple[int, int]], PathFindingTile]

    def __init__(self,
                 path_dict: Dict[Tuple[Tuple[int, int], Tuple[int, int]], PathFindingTile],
                 piece: IPiece,
                 position: Vector2):
        self.paths = path_dict
        self.piece = piece
        self.position = position
