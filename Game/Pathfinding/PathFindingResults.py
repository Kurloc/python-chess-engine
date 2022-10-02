from typing import Dict, TypeAlias, Tuple

from Game.Pathfinding.PathfindingTile import PathFindingTile

#                                    MoveDir       Position
PathFindingResults: TypeAlias = Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]]
