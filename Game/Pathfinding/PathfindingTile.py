from Game.Pieces.IPiece import IPiece
from Game.Pathfinding.Vector2 import Vector2


class PathFindingTile:
    is_attackable: bool = False
    is_blocked: bool = False
    is_enemy: bool = False
    position: Vector2
    piece: IPiece = None

    def __init__(self,
                 attackable: bool,
                 is_blocked: bool,
                 is_enemy: bool,
                 position_of_tile: Vector2,
                 piece_on_tile: IPiece = None):
        self.is_attackable = attackable
        self.is_blocked = is_blocked
        self.is_enemy = is_enemy
        self.position = position_of_tile
        self.piece = piece_on_tile
