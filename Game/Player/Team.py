from __future__ import annotations

from Game.Player.PlayerStartPositions import PlayerStartPositions
from Game.Tile.TileColors import TileColors


class Team:
    color: TileColors
    side: PlayerStartPositions
    team_id: int

    def __init__(self, color: TileColors, side: PlayerStartPositions, player_id: int):
        self.color = color
        self.side = side
        self.team_id = player_id

    def __eq__(self, other: Team) -> bool:
        return self.color == other.color and self.side == other.side
