from typing import List

from Game.Pieces.ChessPieces import ChessPieces
from Game.Player.PlayerStartPositions import PlayerStartPositions
from Game.Pieces.IPiece import IPiece
from Game.Pieces.PieceMove import Move
from Game.Player.Team import Team
from Pathfinding.Vector2 import Vector2


class Pawn(IPiece):
    __move_directions: List[Move]

    def __init__(self, team: Team):
        super().__init__(team, ChessPieces.PAWN)
        self.__move_directions = []
        if team.side == PlayerStartPositions.TOP:
            self.__move_directions.append(Move(Vector2.Up(), 2))
        else:
            self.__move_directions.append(Move(Vector2.Down(), 2))

    @property
    def move_directions(self) -> List[Move]:
        return self.__move_directions

    @property
    def attack_directions(self) -> List[Move]:
        return [Move(Vector2.UpLeft()), Move(Vector2.UpRight())]
