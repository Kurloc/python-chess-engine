import abc
from typing import Dict, Tuple, Union

from Game.Board import Board
from Game.Pathfinding.Vector2 import Vector2
from Game.Pieces.ChessPieces import ChessPieces
from Game.Pieces.IPiece import MoveResult, AttackResult
from Game.Player.PlayerPathDict import PlayerPathDict
from Game.Tile.Tile import Tile


class IChessEngineUser(abc.ABC):
    board: Board

    def __init__(self, board: Board):
        self.board = board

    @abc.abstractmethod
    def input_player_move_input(self,
                                paths: Dict[Tuple[int, int], PlayerPathDict]) -> Tuple[Vector2, Vector2, Vector2]:
        pass

    @abc.abstractmethod
    def input_piece_can_be_upgraded(self) -> ChessPieces:
        pass

    @abc.abstractmethod
    def output_board_state(self, board: Dict[Tuple[int, int], Tile], board_size: Tuple[int, int]) -> None:
        pass

    @abc.abstractmethod
    def output_player_turn_started(self, player_id: int) -> None:
        pass

    @abc.abstractmethod
    def output_player_move_result(self, move_result: MoveResult) -> None:
        pass

    @abc.abstractmethod
    def output_invalid_player_move(self, attack_result: AttackResult) -> None:
        pass

    @abc.abstractmethod
    def output_player_victory(self, winning_player_id: int, move_result: MoveResult, board: Board) -> None:
        pass

    @staticmethod
    def get_move_set_vector(
            from_pos: Tuple[int, int],
            to_position: Tuple[int, int],
            all_paths_for_player: Dict[Tuple[int, int], PlayerPathDict]
    ) -> Union[Vector2, None]:
        keys = all_paths_for_player.keys()
        for key in keys:
            if key != from_pos:
                continue

            value = all_paths_for_player[key]
            path_keys = value.paths.keys()
            for k in path_keys:
                v = value.paths[k]
                for move in v:
                    if move == to_position:
                        return Vector2(key[0], key[1])

        return None
