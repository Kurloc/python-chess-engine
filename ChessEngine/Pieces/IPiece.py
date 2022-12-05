import abc

from typing import List

from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Pieces.PieceMove import Move
from ChessEngine.Player.Team import Team

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

