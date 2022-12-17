from dataclasses import dataclass
from typing import Union, Dict, Self, cast, Tuple

from ChessEngine.Board.WinConditions import WinConditions
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Player.Team import Team
from ChessEngine.Pydantic.TupleToString import tuple_to_string, string_to_tuple


@dataclass
class GameState:
    game_over: bool = False
    winning_team: Union[Team, None] = None
    win_condition: Union[WinConditions, None] = None
    winning_tile_pos: Union[Vector2, None] = None

    @staticmethod
    def from_dict(incoming_value: Dict):
        return GameState(
            incoming_value.get('game_over'),
            Team.from_dict(incoming_value.get('winning_team')),
            WinConditions(incoming_value.get('win_condition')),
            Vector2.from_tuple(cast(Tuple[int, int], string_to_tuple(incoming_value.get('winning_tile_pos'))))
        )

    def to_dict(self) -> Self:
        return {
            'game_over': self.game_over,
            'winning_team': (
                None if self.winning_team is None
                else self.winning_team.to_dict()
            ),
            'win_condition': self.win_condition.value,
            'winning_tile_pos': tuple_to_string(self.winning_tile_pos.get_tuple())
        }
