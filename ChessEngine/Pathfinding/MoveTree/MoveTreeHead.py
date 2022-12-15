from typing import Dict, Tuple

from ChessEngine.Pathfinding.MoveTree.MoveTreeLeaf import MoveTreeLeaf


class MoveTreeHead:
    leaves: Dict[Tuple[int, int], MoveTreeLeaf]
    depth: int = 0
    max_depth: int = 32

    def __init__(self, max_depth: int = 32):
        self.leaves = {}
        self.max_depth = max_depth
