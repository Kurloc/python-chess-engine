from typing import List

from Game.Pieces.ChessPieces import ChessPieces
from Game.Pieces.IPiece import IPiece
from Game.Pieces.PieceMove import Move
from Game.Player.Team import Team
from Pathfinding.Vector2 import Vector2


class Queen(IPiece):
    __move_directions: List[Move]

    def __init__(self, team: Team):
        """
        |0|1|2|3|4|5|6|7|8|
        |1|x| | | |x| | | |
        |2| |x| | |x| | |x|
        |3| | |x| |x| |x| |
        |4| | | |x|x|x| | |
        |5|x|x|x|x|Q|x|x|x|
        |6| | | |x|x|x| | |
        |7| | |x| |x| |x| |
        |8| |x| | |x| | |x|
        :param team:
        """
        super().__init__(team, ChessPieces.QUEEN)
        self.__move_directions = []
        self.__move_directions.append(Move(Vector2.Up(), self.int_inf))
        self.__move_directions.append(Move(Vector2.Down(), self.int_inf))
        self.__move_directions.append(Move(Vector2.Left(), self.int_inf))
        self.__move_directions.append(Move(Vector2.Right(), self.int_inf))
        self.__move_directions.append(Move(Vector2.UpLeft(), self.int_inf))
        self.__move_directions.append(Move(Vector2.UpRight(), self.int_inf))
        self.__move_directions.append(Move(Vector2.DownLeft(), self.int_inf))
        self.__move_directions.append(Move(Vector2.DownRight(), self.int_inf))

    @property
    def move_directions(self) -> List[Move]:
        return self.__move_directions

    @property
    def attack_directions(self) -> List[Move]:
        return []
