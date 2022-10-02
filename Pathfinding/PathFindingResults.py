from typing import Dict, TypeAlias, Tuple

from Pathfinding.PathfindingTile import PathFindingTile

#                                    MoveDir       Position
PathFindingResults: TypeAlias = Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]]
