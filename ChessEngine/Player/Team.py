from __future__ import annotations

from dataclasses import dataclass

import pydantic
from pydantic import BaseModel

from ChessEngine.Player.PlayerStartPositions import PlayerStartPositions
from ChessEngine.Pydantic.ArbitraryConfig import Config
from ChessEngine.Tile.TileColors import TileColors


class Team(BaseModel):
    color: TileColors
    side: PlayerStartPositions
    team_id: int

    def __init__(self,
                 color: TileColors,
                 side: PlayerStartPositions,
                 team_id: int,
                 *args,
                 **kwargs):
        super().__init__(color=color, side=side, team_id=team_id, *args, **kwargs)

    def __eq__(self, other: Team) -> bool:
        return self.color == other.color and self.side == other.side

    def to_dict(self):
        return {
            "color": self.color,
            "side": self.side,
            "team_id": self.team_id
        }

    @staticmethod
    def from_dict(value: dict):
        return Team(value["color"], value["side"], value["team_id"])
