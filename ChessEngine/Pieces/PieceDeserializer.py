from typing import Dict

from ChessEngine.Pieces.Bishop import Bishop
from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Pieces.King import King
from ChessEngine.Pieces.Knight import Knight
from ChessEngine.Pieces.Pawn import Pawn
from ChessEngine.Pieces.Queen import Queen
from ChessEngine.Pieces.Rook import Rook
from ChessEngine.Player.Team import Team


class PieceDeserializer:
    @staticmethod
    def from_dict(input: Dict):
        team = Team.from_dict(input["team"])
        match input["chess_piece"]:
            case ChessPieces.PAWN.value:
                return Pawn(team, input["piece_id"])
            case ChessPieces.ROOK.value:
                return Rook(team, input["piece_id"])
            case ChessPieces.KING.value:
                return King(team, input["piece_id"])
            case ChessPieces.QUEEN.value:
                return Queen(team, input["piece_id"])
            case ChessPieces.KNIGHT.value:
                return Knight(team, input["piece_id"])
            case ChessPieces.BISHOP.value:
                return Bishop(team, input["piece_id"])
