from typing import Tuple, Dict, List

from ChessEngine.Board.Board import Board
from ChessEngine.Engine import Engine
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Player.Player import Player
from ChessEngine.Player.PlayerPathDict import PlayerPathDict


class ChessEngineService:
    __board: Board
    game_running = False
    piece_maps = {
        'unicode': {
        "1_1": "♙",
        "1_2": "♖",
        "1_3": "♘",
        "1_4": "♗",
        "1_5": "♕",
        "1_6": "♔",
        "2_1": "♟",
        "2_2": "♜",
        "2_3": "♞",
        "2_4": "♝",
        "2_5": "♛",
        "2_6": "♚"
    },
        'ascii': {
            "1_1": "p",
            "1_2": "r",
            "1_3": "n",
            "1_4": "♗",
            "1_5": "♕",
            "1_6": "♔",
            "2_1": "P",
            "2_2": "R",
            "2_3": "N",
            "2_4": "B",
            "2_5": "Q",
            "2_6": "K"
        }
    }
    chess_piece_map = {
        "1_1": "♙",
        "1_2": "♖",
        "1_3": "♘",
        "1_4": "♗",
        "1_5": "♕",
        "1_6": "♔",
        "2_1": "♟",
        "2_2": "♜",
        "2_3": "♞",
        "2_4": "♝",
        "2_5": "♛",
        "2_6": "♚"
    }
    player_move: Tuple[Vector2, Vector2] = None
    current_players_moves: Dict[Tuple[int, int], PlayerPathDict] = {}
    chess_engine: Engine

    def __init__(self):
        self.__board = Board()
        self.chess_engine = Engine(self.__board)

    def start_game(self, players: List[Player]):
        self.game_running = True
        self.chess_engine.start_game(
            run_in_background=True,
            players=players,
            board=self.__board
        )

    def stop_game(self):
        self.game_running = False
        self.chess_engine.stop_game()

    @property
    def board(self) -> Board:
        return self.__board
