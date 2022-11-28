from typing import Tuple, List

from Game.Board import Board
from Game.Pathfinding.Vector2 import Vector2
from Game.Pieces.IPiece import IPiece, MoveResult
from Game.Player.PlayerStartPositions import PlayerStartPositions
from Game.Player.Team import Team
from Game.PrintDebugger import PrintDebugger
from Game.Tile.TileColors import TileColors


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
