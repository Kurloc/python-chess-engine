from ChessEngine.Pathfinding.Vector2 import Vector2


class Move:
    vector2: Vector2
    maxDistance: int
    move_can_be_used_as_an_attack: bool = True
    is_attack_only: bool = True
    is_initial_move = False

    def __init__(self,
                 vector2: Vector2,
                 maxDistance: int = 1,
                 is_attack: bool = True,
                 is_attack_only: bool = False,
                 is_initial_move: bool = False):
        self.vector2 = vector2
        self.maxDistance = maxDistance
        self.move_can_be_used_as_an_attack = is_attack
        self.is_attack_only = is_attack_only
        self.is_initial_move = is_initial_move
