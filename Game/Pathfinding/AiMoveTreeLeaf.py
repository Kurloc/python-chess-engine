from __future__ import annotations

from typing import Dict, Tuple

from Game.Board import Board
from Game.Pathfinding.Vector2 import Vector2


class AiMoveTreeLeaf:
    player_one: int
    player_two: int
    starting_position: Vector2
    ending_position: Vector2
    child_ai_move: Dict[Tuple[int, int], AiMoveTreeLeaf]
    turn_chain: [int] = []
    board: Board

    def __init__(self,
                 player_one: int,
                 player_two: int,
                 starting_position: Vector2,
                 ending_position: Vector2,
                 board: Board = None
                 ):
        self.player_one = player_one
        self.player_two = player_two
        self.starting_position = starting_position
        self.ending_position = ending_position
        self.board = board
        self.child_ai_move = {}


class AiMoveTreeHead:
    leaves: Dict[Tuple[int, int], AiMoveTreeLeaf]
    depth: int = 0
    max_depth: int = 32

    def __init__(self, max_depth: int = 32):
        self.leaves = {}
        self.max_depth = max_depth


class LeafResult:
    player_one: int
    player_two: int
    turn_chain: [(int, int, int, int)]
    turns: int

    def __init__(self,
                 player_one: int,
                 player_two: int,
                 turns: int,
                 turn_chain: [(int, int, int, int)] = None):
        self.player_one = player_one
        self.player_two = player_two
        self.turns = turns
        if turn_chain is None:
            self.turn_chain = []
        else:
            self.turn_chain = turn_chain

    def add_turn(self, start: Vector2, end: Vector2):
        self.turn_chain.append((start.x, start.y, end.x, end.y))
