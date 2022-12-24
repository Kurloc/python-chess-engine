import time
from typing import Dict, Tuple

from ChessEngine.Board.AttackResult import AttackResult
from ChessEngine.Board.Board import Board
from ChessEngine.Board.BoardState import BoardState
from ChessEngine.Board.MoveResult import MoveResult
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Player.IChessEngineUser import IChessEngineUser, PlayerTurnStart, PlayerVictory
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from TextualClient.Sockets.PlayerManagement import PlayerManagement


class TextualOfflineEngineUser(IChessEngineUser):

    def __init__(
            self,
            board: Board,
            player_management: PlayerManagement
    ):
        super().__init__(board)
        self.player_management = player_management

    def input_piece_can_be_upgraded(self) -> ChessPieces:
        self.player_management.show_piece_upgrade_window.on_next(True)
        self.player_management.need_selection.on_next(True)

        while self.player_management.need_selection.value and self.player_management.game_running.value:
            piece_selection = self.player_management.piece_selection.value
            if piece_selection is None or piece_selection == ChessPieces.NONE:
                time.sleep(.15)
            else:
                self.player_management.need_selection.on_next(False)
                self.player_management.show_piece_upgrade_window.on_next(False)

        return self.player_management.piece_selection.value

    def input_player_move_input(
            self,
            paths: Dict[Tuple[int, int], PlayerPathDict]
    ) -> Tuple[Vector2, Vector2]:
        self.player_management.current_players_moves.on_next(paths)
        while True:
            time.sleep(.15)
            if self.player_management.player_move.value is not None:
                break

        return_value = self.player_management.player_move.value
        self.player_management.player_move.on_next(None)

        return return_value

    def output_board_state(self, board_state: BoardState) -> None:
        self.player_management.board_state.on_next(board_state.board)

    def output_player_turn_started(self, player_turn_start: PlayerTurnStart) -> None:
        self.player_management.current_team_id.on_next(player_turn_start.player_id)

    def output_player_move_result(self, move_result: MoveResult) -> None:
        pass

    def output_invalid_player_move(self, attack_result: AttackResult) -> None:
        pass

    def output_player_victory(self, player_victory: PlayerVictory) -> None:
        self.player_management.player_victory.on_next(player_victory)
