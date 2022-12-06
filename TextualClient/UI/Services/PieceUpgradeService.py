from dataclasses import dataclass

from ChessEngine.Pieces.ChessPieces import ChessPieces


@dataclass
class PieceUpgradeService:
    piece_selection: ChessPieces = ChessPieces.NONE
    need_selection: bool = False
