from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pathfinding.Vector2 import Vector2


class PathFindingTile:
    move_can_be_used_as_an_attack: bool = False
    is_blocked: bool = False
    is_enemy: bool = False
    is_attack_only: bool = False
    position: Vector2
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
