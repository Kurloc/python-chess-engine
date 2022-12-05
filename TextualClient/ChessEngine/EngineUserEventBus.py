import abc
import time
import traceback
from typing import Dict, Tuple

from textual.css.query import NoMatches

from ChessEngine.Board.Board import Board
from ChessEngine.Board.MoveResult import MoveResult
from ChessEngine.Debugging.PrintDebugger import PrintDebugger
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from ChessEngine.Tile.Tile import Tile
from TextualClient.UI.Widgets.GameHeader import GameHeader


class EngineUserEventBus(abc.ABC):
    def __init__(self, game):
        self.game = game

    def input_player_move_input(
            self,
            paths: Dict[Tuple[int, int], PlayerPathDict]
    ) -> Tuple[Vector2, Vector2]:
        self.game.chess_engine_service.current_players_moves = paths
        while self.game.chess_engine_service.player_move is None and self.game.chess_engine_service.game_running:
            time.sleep(.15)

        assert self.game.chess_engine_service.player_move is not None
        return_value = self.game.chess_engine_service.player_move
        self.game.chess_engine_service.player_move = None

        return return_value

    def on_piece_can_be_upgraded(self) -> ChessPieces:
        self.game.show_piece_upgrade_window()
        self.game.piece_upgrade_service.need_selection = True
        while self.game.piece_upgrade_service.need_selection and self.game.chess_engine_service.game_running:
            piece_selection = self.game.piece_upgrade_service.piece_selection
            if piece_selection is None or piece_selection == ChessPieces.NONE:
                time.sleep(.15)
            else:
                self.game.piece_upgrade_service.need_selection = False
                self.game.hide_piece_upgrade_window()

        return self.game.piece_upgrade_service.piece_selection

    def on_output_player_turn_started(self, player_id: int) -> None:
        if player_id == 1:
            team = self.game.chess_engine_service.board.teams[0]
        else:
            team = self.game.chess_engine_service.board.teams[1]

        self.game.query_one(GameHeader).turn_string = f'{team.color.name}\'s turn'
        self.game.query_one(GameHeader).mf = (0, 0)
        self.game.query_one(GameHeader).mt = (0, 0)

    def on_output_player_move_result(
            self,
            board: Dict[Tuple[int, int], Tile]
    ):
        for tile in board:
            tile = board[tile]
            piece = tile.piece
            pos = tile.position
            if piece is not None:
                cell_text = self.game\
                    .chess_engine_service\
                    .chess_piece_map\
                    .get(f"{piece.team.team_id}_{piece.chess_piece}", "")
            else:
                cell_text = ""
            try:
                self.game.cell(pos.x, pos.y).label = cell_text
            except NoMatches:
                pass

    def on_output_board_state(
            self,
            board: Dict[Tuple[int, int], Tile],
            board_size: Tuple[int, int]
    ) -> None:
        pass

    def on_output_player_victory(
            self,
            winning_player_id: int,
            move_result: MoveResult,
            board: Board
    ) -> None:
        self.game.show_piece_winner_window(
            winning_player_id=winning_player_id,
            move_result_str=PrintDebugger.print_move_results(move_result),
            print_string=f'Player {winning_player_id} has won!'
        )
