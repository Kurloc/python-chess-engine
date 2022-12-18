from typing import List

from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pieces.PieceMove import Move
from ChessEngine.Player.Team import Team
from ChessEngine.Pathfinding.Vector2 import Vector2


class Rook(IPiece):
    __move_directions: List[Move]

    def __init__(self, team: Team, piece_id: int = None):
        self.__move_directions = []
        self.__move_directions.append(Move(Vector2.Up(), self.int_inf))
        self.__move_directions.append(Move(Vector2.Down(), self.int_inf))
        self.__move_directions.append(Move(Vector2.Left(), self.int_inf))
        self.__move_directions.append(Move(Vector2.Right(), self.int_inf))
        super().__init__(team, piece_id)

    @property
    def chess_piece(self) -> ChessPieces:
        return ChessPieces.ROOK

    @property
    def move_directions(self) -> List[Move]:
        return self.__move_directions
