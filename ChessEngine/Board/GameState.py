from typing import Union

from ChessEngine.Board.WinConditions import WinConditions
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Player.Team import Team


class GameState:
    game_over: bool = False
    winning_team: Union[Team, None] = None
    win_condition: Union[WinConditions, None] = None
    winning_tile_pos: Union[Vector2, None] = None
