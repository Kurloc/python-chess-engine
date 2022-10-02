from Game.Pathfinding.Vector2 import Vector2


class Move:
    vector2: Vector2
    maxDistance: int

    def __init__(self, vector2: Vector2, maxDistance: int = 1):
        self.vector2 = vector2
        self.maxDistance = maxDistance
