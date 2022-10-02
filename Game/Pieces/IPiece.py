import abc
from enum import Enum

from typing import List, Union

from Game.Pieces.ChessPieces import ChessPieces
from Game.Pieces.PieceMove import Move
from Game.Player.Team import Team
from Game.Pathfinding.Vector2 import Vector2


class IPiece(abc.ABC):
    team: Team
    chess_piece: ChessPieces
    int_inf = int(2147483647)

    def __init__(self, team: Team, chess_piece: ChessPieces):
        self.team = team
        self.chess_piece = chess_piece

    @property
    def move_directions(self) -> List[Move]:
        return []

    @property
    def attack_directions(self) -> List[Move]:
        return []

    @property
    def is_blockable(self) -> bool:
        return True


class BoardEventTypes(Enum):
    INVALID_MOVE = 0
    PIECE_BLOCKED_BY_ALLY = 1
    PIECE_BLOCKED_BY_ENEMY = 1
    PIECE_MOVED_TO_SPACE = 2
    PIECE_MOVED_TO_SPACE_AND_KILLED = 3


class BoardEventPiece:
    piece: IPiece
    starting_position: [Vector2, None]
    ending_position: Union[Vector2, None]

    def __init__(self, piece: IPiece,
                 starting_position: Union[Vector2, None] = None,
                 ending_position: Union[Vector2, None] = None):
        self.piece = piece
        self.starting_position = starting_position
        self.ending_position = ending_position


class BoardEvent:
    event_type: BoardEventTypes
    pieces_involved: List[BoardEventPiece]
    turn_index: int
    move_to_position: Vector2

    def __init__(self,
                 event_type: BoardEventTypes,
                 pieces_involved: List[BoardEventPiece],
                 move_to_position: Vector2,
                 turn_index: int):
        self.event_type = event_type
        self.pieces_involved = pieces_involved
        self.move_to_position = move_to_position
        self.turn_index = turn_index


class AttackResult:
    success: bool = False
    board_event_type: BoardEventTypes
    pieces_involved: List[BoardEventPiece]

    def __init__(self,
                 success: bool,
                 board_event_type: BoardEventTypes,
                 pieces_involved: List[BoardEventPiece] = None):
        if pieces_involved is None:
            pieces_involved = []

        self.success = success
        self.board_event_type = board_event_type
        self.pieces_involved = pieces_involved

class WinConditions(Enum):
    CHECKMATE = 0
    STALEMATE = 1
    RESIGNATION = 2
    TIME_OUT = 3

class GameState:
    game_over: bool = False
    winning_team: Union[Team, None] = None
    win_condition: Union[WinConditions, None] = None
    winning_tile_pos: Union[Vector2, None] = None


class MoveResult(AttackResult):
    game_state: GameState

    def __init__(self,
                 game_state: GameState,
                 attack_result: AttackResult):
        super().__init__(attack_result.success, attack_result.board_event_type, attack_result.pieces_involved)
        self.game_state = game_state
