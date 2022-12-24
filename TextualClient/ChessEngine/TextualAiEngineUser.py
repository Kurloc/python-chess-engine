from ChessEngine.Board.AttackResult import AttackResult
from ChessEngine.Board.Board import Board
from ChessEngine.Board.BoardState import BoardState
from ChessEngine.Board.MoveResult import MoveResult
from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Player.AI.AIEngineUser import AiEngineUser
from ChessEngine.Player.IChessEngineUser import PlayerTurnStart, PlayerVictory
from TextualClient.Sockets.PlayerManagement import PlayerManagement


class TextualAiEngineUser(AiEngineUser):
    player_management: PlayerManagement

    def __init__(
            self,
            board: Board,
            player_management: PlayerManagement
    ):
        super().__init__(board, board.teams, 5)
        self.player_management = player_management

    def input_piece_can_be_upgraded(self) -> ChessPieces:
        return super().input_piece_can_be_upgraded()

    def output_board_state(self, board_state: BoardState) -> None:
        self.player_management.board_state.on_next(board_state.board)

    def output_player_turn_started(self, player_turn_start: PlayerTurnStart) -> None:
        super().output_player_turn_started(player_turn_start)
        self.player_management.current_team_id.on_next(player_turn_start.player_id)

    def output_player_move_result(self, move_result: MoveResult) -> None:
        pass

    def output_invalid_player_move(self, attack_result: AttackResult) -> None:
        pass

    def output_player_victory(self, player_victory: PlayerVictory) -> None:
        self.player_management.player_victory.on_next(player_victory)
