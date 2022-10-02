import abc
from typing import Dict, Tuple

from Game.Player.PlayerPathDict import PlayerPathDict
from Game.Pieces.IPiece import MoveResult, AttackResult
from Game.Tile.Tile import Tile
from Game.Pathfinding.PathfindingTile import PathFindingTile
from Game.Pathfinding.Vector2 import Vector2


class IChessEngineUser(abc.ABC):
    @abc.abstractmethod
    def input_player_move_input(self,
                                player_id: int,
                                paths: Dict[Tuple[int, int], PlayerPathDict]) -> Tuple[Vector2, Vector2, Vector2]:
        pass

    @abc.abstractmethod
    def output_board_state(self, board: Dict[Tuple[int, int], Tile]) -> None:
        pass

    @abc.abstractmethod
    def output_player_turn_started(self, player_id: int) -> None:
        pass

    @abc.abstractmethod
    def output_player_move_result(self, move_result: MoveResult) -> None:
        pass

    @abc.abstractmethod
    def output_invalid_player_move(self, player_id: int, attack_result: AttackResult) -> None:
        pass

    @abc.abstractmethod
    def output_current_tile_paths(self, paths: Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]]) -> None:
        pass
