from Game.Pieces.IPiece import IPiece
from Game.Pathfinding.Vector2 import Vector2


class PathFindingTile:
    attackable: bool = False
    isBlocked: bool = False
    isEnemy: bool = False
    position: Vector2
    piece: IPiece = None

    def __init__(self,
                 attackable: bool,
                 is_blocked: bool,
                 is_enemy: bool,
                 position_of_tile: Vector2,
                 piece_on_tile: IPiece = None):
        self.attackable = attackable
        self.isBlocked = is_blocked
        self.isEnemy = is_enemy
        self.position = position_of_tile
        self.piece = piece_on_tile
