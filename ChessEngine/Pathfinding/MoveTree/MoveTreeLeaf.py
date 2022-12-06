from __future__ import annotations

from typing import Dict, Tuple

from ChessEngine.Board.Board import Board
from ChessEngine.Pathfinding.Vector2 import Vector2


class MoveTreeLeaf:
    player_one: int
    player_two: int
    starting_position: Vector2
    ending_position: Vector2
    child_ai_move: Dict[Tuple[int, int], MoveTreeLeaf]
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
