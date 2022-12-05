from typing import List

from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pieces.PieceMove import Move
from ChessEngine.Player.Team import Team
from ChessEngine.Pathfinding.Vector2 import Vector2


class King(IPiece):
    __move_directions: List[Move]

    def __init__(self, team: Team, piece_id: int = None):
        super().__init__(team, piece_id)
        """
        |0|1|2|3|4|5|6|7|8|
        |1| | | | | | | | |
        |2| | | | | | | | |
        |3| | | |1|x|2| | |
        |4| | |8|x|x|x|3| |
        |5| | |x|x|k|x|x| |
        |6| | |7|x|x|x|4| |
        |7| | | |6|x|5| | |
        |8| | | | | | | | |
        :param team:
        """
        self.__move_directions = []
        self.__move_directions.append(Move(Vector2.Up()))
        self.__move_directions.append(Move(Vector2.Down()))
        self.__move_directions.append(Move(Vector2.Left()))
        self.__move_directions.append(Move(Vector2.UpLeft()))
        self.__move_directions.append(Move(Vector2.DownLeft()))
        self.__move_directions.append(Move(Vector2.UpRight()))
        self.__move_directions.append(Move(Vector2.Right()))
        self.__move_directions.append(Move(Vector2.DownRight()))

    @property
    def chess_piece(self) -> ChessPieces:
        return ChessPieces.KING

    @property
    def move_directions(self) -> List[Move]:
        return self.__move_directions
