from typing import Tuple

from ChessEngine.Pathfinding.Vector2 import Vector2


class LeafResult:
    player_one: int
    player_two: int
    turn_chain: [Tuple[int, int, int, int]]
    turns: int

    def __init__(self,
                 player_one: int,
                 player_two: int,
                 turns: int,
                 turn_chain: [Tuple[int, int, int, int]] = None):
        self.player_one = player_one
        self.player_two = player_two
        self.turns = turns
        if turn_chain is None:
            self.turn_chain = []
        else:
            self.turn_chain = turn_chain

    def add_turn(self, start: Vector2, end: Vector2):
        self.turn_chain.append((start.x, start.y, end.x, end.y))
