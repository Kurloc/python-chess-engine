import abc
from dataclasses import dataclass

from typing import List, Dict

import pydantic

from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Pieces.PieceMove import Move
from ChessEngine.Player.Team import Team
from ChessEngine.Pydantic.ArbitraryConfig import Config


@dataclass
class IPiece(abc.ABC):
    __piece_id = 0
    __return_piece_id = 0
    piece_id: int
    team: Team
    int_inf = int(2147483647)

    def __init__(self, team: Team, piece_id: int = None):
        self.team = team
        if piece_id is None:
            self.piece_id = IPiece.__piece_id + 1
            IPiece.__piece_id += 1
        else:
            self.piece_id = piece_id

    @property
    def chess_piece(self) -> ChessPieces:
        return ChessPieces.NONE

    @property
    def move_directions(self) -> List[Move]:
        return []

    @property
    def is_blockable(self) -> bool:
        return True

    def to_dict(self):
        return {
            "piece_id": self.piece_id,
            "team": self.team.to_dict(),
            "chess_piece": self.chess_piece,
            "move_directions": [x.to_dict() for x in self.move_directions],
            "is_blockable": self.is_blockable
        }

    @staticmethod
    def copy(team: Team):
        return IPiece(team)

    @staticmethod
    def from_dict(piece_Value: Dict):
        piece_id = piece_Value["piece_id"]
        team = Team.from_dict(piece_Value["team"])
        return IPiece(team, piece_id)
