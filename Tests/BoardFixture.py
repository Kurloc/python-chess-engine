from typing import Tuple, List

from ChessEngine.Board.Board import Board
from ChessEngine.Board.MoveResult import MoveResult
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Player.PlayerStartPositions import PlayerStartPositions
from ChessEngine.Player.Team import Team
from ChessEngine.Debugging.PrintDebugger import PrintDebugger
from ChessEngine.Tile.TileColors import TileColors


class BoardFixture:
    board: Board
    teams: List[Team] = [
        Team(TileColors.WHITE, PlayerStartPositions.TOP, 1),
        Team(TileColors.BLACK, PlayerStartPositions.BOTTOM, 2)
    ]

    def __init__(self, piece_map: [[IPiece]] = None, teams: List[Team] = None):
        if teams is None:
            self.teams = [
                Team(TileColors.WHITE, PlayerStartPositions.TOP, 1),
                Team(TileColors.BLACK, PlayerStartPositions.BOTTOM, 2)
            ]

        if piece_map is None:
            self.board = Board()

        if piece_map is not None:
            self.board = Board(piece_map, teams=self.teams)

    def move_piece(self,
                   start_pos: Tuple[int, int],
                   end_pos: Tuple[int, int],
                   board: Board = None,
                   team_id: int = None) -> MoveResult:
        if board is None:
            board = self.board

        if team_id is None:
            team_id = board.map[start_pos].piece.team.team_id

        tile = board.map[start_pos]
        pathfinding_results = board.find_paths(tile)
        move_results = board.move_piece(tile, Vector2(end_pos[0], end_pos[1]), pathfinding_results, team_id)

        PrintDebugger.print_board(board.map, board.game_board_size)

        return move_results
