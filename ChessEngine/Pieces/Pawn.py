from typing import List

from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Player.PlayerStartPositions import PlayerStartPositions
from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pieces.PieceMove import Move
from ChessEngine.Player.Team import Team
from ChessEngine.Pathfinding.Vector2 import Vector2


class Pawn(IPiece):
    __move_directions: List[Move]

    def __init__(self, team: Team, piece_id: int = None):
        super().__init__(team, piece_id)
        if team.side == PlayerStartPositions.TOP:
            self.__move_directions = [
                Move(Vector2.Up(), 1, False),
                Move(Vector2.Up() * 2, 1, False, is_initial_move=True),
                Move(Vector2.UpLeft(), 1, True, True),
                Move(Vector2.UpRight(), 1, True, True),
            ]
        else:
            self.__move_directions = [
                Move(Vector2.Down(), 1, False),
                Move(Vector2.Down() * 2, 1, False, is_initial_move=True),
                Move(Vector2.DownLeft(), 1, True, True),
                Move(Vector2.DownRight(), 1, True, True),
            ]

    @property
    def chess_piece(self) -> ChessPieces:
        return ChessPieces.PAWN

    @property
    def move_directions(self) -> List[Move]:
        return self.__move_directions
