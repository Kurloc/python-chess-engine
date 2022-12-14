from typing import List

from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pieces.PieceMove import Move
from ChessEngine.Player.Team import Team
from ChessEngine.Pathfinding.Vector2 import Vector2


class Bishop(IPiece):
    __move_directions: List[Move] = []

    def __init__(self, team: Team, piece_id: int = None):
        super().__init__(team, piece_id)
        self.__move_directions.append(Move(Vector2.UpLeft(), self.int_inf))
        self.__move_directions.append(Move(Vector2.UpRight(), self.int_inf))
        self.__move_directions.append(Move(Vector2.DownLeft(), self.int_inf))
        self.__move_directions.append(Move(Vector2.DownRight(), self.int_inf))

    @property
    def chess_piece(self) -> ChessPieces:
        return ChessPieces.BISHOP

    @property
    def move_directions(self) -> List[Move]:
        return self.__move_directions
