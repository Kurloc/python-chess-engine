from ChessEngine.Board.AttackResult import AttackResult
from ChessEngine.Board.GameState import GameState


class MoveResult(AttackResult):
    game_state: GameState
    piece_can_be_upgraded: bool

    def __init__(self,
                 game_state: GameState,
                 attack_result: AttackResult,
                 piece_can_be_upgraded: bool = False):
        super().__init__(attack_result.success, attack_result.board_event_type, attack_result.pieces_involved)
        self.game_state = game_state
        self.piece_can_be_upgraded = piece_can_be_upgraded
