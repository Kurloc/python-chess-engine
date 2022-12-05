from typing import Dict, Tuple

from ChessEngine.Board.AttackResult import AttackResult
from ChessEngine.Board.Board import Board
from ChessEngine.Board.MoveResult import MoveResult
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Player.AI.AIEngineUser import AiEngineUser
from ChessEngine.Player.IChessEngineUser import IChessEngineUser
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from ChessEngine.Tile.Tile import Tile
from TextualClient.ChessEngine.EngineUserEventBus import EngineUserEventBus


class TextualAiEngineUser(AiEngineUser):
    engine_user_event_bus: EngineUserEventBus

    def __init__(self, engine_user_event_bus: EngineUserEventBus, board: Board):
        super().__init__(board, board.teams, 5)
        self.engine_user_event_bus = engine_user_event_bus
        with open('../../constructed.txt', 'w') as f:
            f.write('constructed engine user')

    def input_piece_can_be_upgraded(self) -> ChessPieces:
        return super().input_piece_can_be_upgraded()

    def output_board_state(
            self,
            board: Dict[Tuple[int, int], Tile],
            board_size: Tuple[int, int]
    ) -> None:
        self.engine_user_event_bus.on_output_player_move_result(
            board
        )

    def output_player_turn_started(self, player_id: int) -> None:
        super().output_player_turn_started(player_id)
        self.engine_user_event_bus.on_output_player_turn_started(player_id)

    def output_player_move_result(self, move_result: MoveResult) -> None:
        pass

    def output_invalid_player_move(self, attack_result: AttackResult) -> None:
        pass

    def output_player_victory(self, winning_player_id: int, move_result: MoveResult, board: Board) -> None:
        self.engine_user_event_bus.on_output_player_victory(winning_player_id, move_result, board)
