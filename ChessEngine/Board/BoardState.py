from __future__ import annotations

import datetime
import traceback
from dataclasses import dataclass
from typing import Dict, Tuple
from typing import Union, List

import pydantic
from pydantic import BaseModel

from ChessEngine.Board.AttackResult import AttackResult
from ChessEngine.Board.Board import Board
from ChessEngine.Board.BoardEvent import BoardEvent
from ChessEngine.Board.BoardEventPiece import BoardEventPiece
from ChessEngine.Board.BoardEventTypes import BoardEventTypes
from ChessEngine.Board.GameState import GameState
from ChessEngine.Board.MoveResult import MoveResult
from ChessEngine.Board.WinConditions import WinConditions
from ChessEngine.Debugging.setup_logger import kce_exception_logger
from ChessEngine.Pathfinding.PathfindingTile import PathFindingTile
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.Bishop import Bishop
from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pieces.King import King
from ChessEngine.Pieces.Knight import Knight
from ChessEngine.Pieces.Pawn import Pawn
from ChessEngine.Pieces.Queen import Queen
from ChessEngine.Pieces.Rook import Rook
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from ChessEngine.Player.PlayerStartPositions import PlayerStartPositions
from ChessEngine.Player.Team import Team
from ChessEngine.Pydantic.ArbitraryConfig import Config
from ChessEngine.Pydantic.TupleToString import tuple_to_string
from ChessEngine.Tile.Tile import Tile
from ChessEngine.Tile.TileColors import TileColors


@pydantic.dataclasses.dataclass(config=Config)
class BoardState(BaseModel):
    board: Dict[Tuple[int, int], Tile]
    board_size: Tuple[int, int]

    def __init__(
            self,
            board: Dict[Tuple[int, int], Tile],
            board_size: Tuple[int, int],
            *args,
            **kwargs
    ):
        super().__init__(
            board=board,
            board_size=board_size,
            *args,
            **kwargs
        )

class PydBoardState(BaseModel):
    board: Dict[str, Tile]
    board_size: Tuple[int, int]

    def __init__(
            self,
            board: Dict[str, Tile],
            board_size: Tuple[int, int],
            *args,
            **kwargs
    ):
        super().__init__(
            board=board,
            board_size=board_size,
            *args,
            **kwargs
        )

    @staticmethod
    def from_board_state(board_state: BoardState):
        string_dict = {}
        for key in board_state.board:
            string_dict[tuple_to_string(key)] = board_state.board[key]

        return PydBoardState(board=string_dict, board_size=board_state.board_size)

    @staticmethod
    def from_board(board: Board):
        string_dict = {}
        for key in board.map:
            string_dict[tuple_to_string(key)] = board.map[key]

        return PydBoardState(board=string_dict, board_size=board.game_board_size)

    def to_board_state(self):
        tup_dict = {}
        for key in self.board:
            tup_dict[tuple(key.split(','))] = self.board[key]

        return BoardState(tup_dict, self.board_size)