from typing import List

from Game.Pieces.ChessPieces import ChessPieces
from Game.Pieces.IPiece import IPiece
from Game.Pieces.PieceMove import Move
from Game.Player.Team import Team
from Game.Pathfinding.Vector2 import Vector2


class Rook(IPiece):
    __move_directions: List[Move]

    def __init__(self, team: Team):
        super().__init__(team, ChessPieces.ROOK)
        self.__move_directions = []
        self.__move_directions.append(Move(Vector2.Up(), self.int_inf))
        self.__move_directions.append(Move(Vector2.Down(), self.int_inf))
        self.__move_directions.append(Move(Vector2.Left(), self.int_inf))
        self.__move_directions.append(Move(Vector2.Right(), self.int_inf))

    @property
    def move_directions(self) -> List[Move]:
        return self.__move_directions

    @property
    def attack_directions(self) -> List[Move]:
        return []
