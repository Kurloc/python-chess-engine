from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pydantic.TupleToString import tuple_to_string, string_to_tuple


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

    def to_dict(self):
        return {
            "vector2": tuple_to_string(self.vector2.get_tuple()),
            "maxDistance": self.maxDistance,
            "move_can_be_used_as_an_attack": self.move_can_be_used_as_an_attack,
            "is_attack_only": self.is_attack_only,
            "is_initial_move": self.is_initial_move
        }

    @staticmethod
    def from_dict(dict: dict):
        return Move(
            vector2=Vector2.from_tuple(string_to_tuple(dict["vector2"])),
            maxDistance=dict["maxDistance"],
            is_attack=dict["move_can_be_used_as_an_attack"],
            is_attack_only=dict["is_attack_only"],
            is_initial_move=dict["is_initial_move"]
        )
