import abc
import json
from dataclasses import dataclass
from enum import Enum, IntEnum

from typing import List, Union

from Game.Pieces.ChessPieces import ChessPieces
from Game.Pieces.PieceMove import Move
from Game.Player.Team import Team
from Game.Pathfinding.Vector2 import Vector2

class IPiece(abc.ABC):
    __piece_id = 0
    __return_piece_id = 0
    team: Team
    int_inf = int(2147483647)

    def __init__(self, team: Team, piece_id: int = None):
        self.team = team
        if piece_id is None:
            self.__return_piece_id = IPiece.__piece_id + 1
            IPiece.__piece_id += 1
        else:
            self.__return_piece_id = piece_id

    @property
    def piece_id(self) -> int:
        return self.__return_piece_id

    @property
    def chess_piece(self) -> ChessPieces:
        return ChessPieces.NONE

    @property
    def move_directions(self) -> List[Move]:
        return []

    @property
    def is_blockable(self) -> bool:
        return True

    @staticmethod
    def copy(team: Team):
        return IPiece(team)


class BoardEventTypes(IntEnum):
    INVALID_MOVE = 0
    INVALID_MOVE_PIECE_CANNOT_DO_MOVE = 1
    INVALID_MOVE_PIECE_CANNOT_DO_THIS_ATTACK = 2
    INVALID_MOVE_ATTACKS_MUST_BE_DONE_ON_ENEMIES = 3
    PIECE_BLOCKED_BY_ALLY = 4
    PIECE_BLOCKED_BY_ENEMY = 5
    PIECE_MOVED_TO_SPACE = 6
    PIECE_MOVED_TO_SPACE_AND_KILLED = 7,
    MOVE_CAN_ONLY_BE_MADE_TO_EMPTY_SPACE = 8


@dataclass
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


@dataclass
class BoardEvent:
    event_type: BoardEventTypes
    pieces_involved: List[BoardEventPiece]
    turn_index: int
    move_to_position: Vector2

    def to_json(self):
        # v = self.__dict__
        # for i in v['pieces_involved']:
        #     t = i.piece
        #
        #     if t is not None:
        #         z = t.__dict__
        #         z['starting_position'] = i.starting_position.__dict__
        #         z['ending_position'] = i.ending_position.__dict__
        #         z['team'] = t.team.__dict__
        #         keys_to_remove = []
        #         for key in z:
        #             if key[0] == '_':
        #                 keys_to_remove.append(key)
        #
        #         for key in keys_to_remove:
        #             del z[key]
        #
        #         v['pieces_involved'] = z
        #
        # print(v)
        # return_json = json.dumps(v, indent=4)
        # return return_json
        return json.dumps(self, indent=4, default=lambda x: x.__dict__)

class WinConditions(Enum):
    MATE = 0
    CHECKMATE = 1
    STALEMATE = 2
    RESIGNATION = 3
    TIME_OUT = 4


class GameState:
    game_over: bool = False
    winning_team: Union[Team, None] = None
    win_condition: Union[WinConditions, None] = None
    winning_tile_pos: Union[Vector2, None] = None


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
