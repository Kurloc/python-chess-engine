import abc
import traceback
from typing import Dict, Tuple, Union

from ChessEngine.Board import Board
from ChessEngine.Board.AttackResult import AttackResult
from ChessEngine.Board.BoardState import BoardState
from ChessEngine.Board.MoveResult import MoveResult
from ChessEngine.Debugging.setup_logger import kce_exception_logger
from ChessEngine.Pathfinding.PathfindingTile import PathFindingTile
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from ChessEngine.Tile.Tile import Tile


class IChessEngineUser(abc.ABC):
    board: Board

    def __init__(self, board: Board):
        self.board = board

    @abc.abstractmethod
    def input_piece_can_be_upgraded(self) -> ChessPieces:
        pass

    @abc.abstractmethod
    def input_player_move_input(
            self,
            paths: Dict[Tuple[int, int], PlayerPathDict]
    ) -> Tuple[Vector2, Vector2]:
        pass

    @abc.abstractmethod
    def output_board_state(self, board_state: BoardState) -> None:
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
    def output_player_victory(
            self,
            winning_player_id: int,
            move_result: MoveResult,
            board: Board
    ) -> None:
        pass

    @staticmethod
    def get_valid_moves_from_paths_for_piece(
            board: Board,
            tile_pos: Tuple[int, int],
            input_paths: Dict[Tuple[int, int], PlayerPathDict]
    ) -> Dict[Tuple[Tuple[int, int], Tuple[int, int]], PathFindingTile]:
        try:
            valid_moves: Dict[Tuple[Tuple[int, int], Tuple[int, int]], PathFindingTile] = {}
            path_sets = input_paths.get(tile_pos, None)
            if path_sets is None:
                return valid_moves

            paths = path_sets.paths
            for path_key in paths:
                path = path_sets.paths[path_key]
                move_result = board.check_if_move_is_valid(
                    board.get_tile_by_tuple(path_key[0]),
                    paths,
                    Vector2(path_key[1][0], path_key[1][1])
                )
                if move_result.success:
                    valid_moves[path_key] = path
            return valid_moves

        except Exception as e:
            from ChessEngine.Debugging.PrintDebugger import PrintDebugger
            tb = traceback.format_exc()
            kce_exception_logger.info('Exception in get_valid_moves_from_paths_for_piece')
            kce_exception_logger.exception(e)
            kce_exception_logger.warning(tb)
            kce_exception_logger.info(PrintDebugger.print_board(board.map, board.game_board_size, False))
            kce_exception_logger.info('============================================================================')
            raise

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
                move = value.paths[k]
                if move == to_position:
                    return Vector2(key[0], key[1])

        return None
