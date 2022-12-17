from typing import Dict, Tuple

from ChessEngine.Board.AttackResult import AttackResult
from ChessEngine.Board.Board import Board
from ChessEngine.Board.BoardState import BoardState
from ChessEngine.Board.MoveResult import MoveResult
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Player.AI.AIEngineUser import AiEngineUser
from ChessEngine.Player.IChessEngineUser import IChessEngineUser, PlayerTurnStart
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from ChessEngine.Tile.Tile import Tile
from TextualClient.ChessEngine.SinglePlayerChessEngineUserEventBus import SinglePlayerChessEngineUserEventBus


class TextualAiEngineUser(AiEngineUser):
    engine_user_event_bus: SinglePlayerChessEngineUserEventBus

    def __init__(self, engine_user_event_bus: SinglePlayerChessEngineUserEventBus, board: Board):
        super().__init__(board, board.teams, 5)
        self.engine_user_event_bus = engine_user_event_bus

    def input_piece_can_be_upgraded(self) -> ChessPieces:
        return super().input_piece_can_be_upgraded()

    def output_board_state(self, board_state: BoardState) -> None:
        self.engine_user_event_bus.on_output_player_move_result(
            board_state.board
        )

    def output_player_turn_started(self, player_turn_start: PlayerTurnStart) -> None:
        super().output_player_turn_started(player_turn_start)
        self.engine_user_event_bus.on_output_player_turn_started(player_turn_start.player_id)

    def output_player_move_result(self, move_result: MoveResult) -> None:
        pass

    def output_invalid_player_move(self, attack_result: AttackResult) -> None:
        pass

    def output_player_victory(self, winning_player_id: int, move_result: MoveResult, board: Board) -> None:
        self.engine_user_event_bus.on_output_player_victory(winning_player_id, move_result, board)
