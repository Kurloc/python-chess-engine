from __future__ import annotations

from Game.Player.PlayerStartPositions import PlayerStartPositions
from Game.Tile.TileColors import TileColors


class Team:
    color: TileColors
    side: PlayerStartPositions

    def __init__(self, color: TileColors, side: PlayerStartPositions):
        self.color = color
        self.side = side

    def __eq__(self, other: Team) -> bool:
        return self.color == other.color and self.side == other.side
