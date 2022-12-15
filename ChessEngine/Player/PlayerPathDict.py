from dataclasses import dataclass
from typing import Dict, Tuple, cast

from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pathfinding.PathfindingTile import PathFindingTile
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.PieceDeserializer import PieceDeserializer
from ChessEngine.Pydantic.TupleToString import tuple_to_string, string_to_tuple


@dataclass
class PlayerPathDict:
    piece: IPiece
    position: Vector2
    paths: Dict[Tuple[Tuple[int, int], Tuple[int, int]], PathFindingTile]

    def __init__(self,
                 path_dict: Dict[Tuple[Tuple[int, int], Tuple[int, int]], PathFindingTile],
                 piece: IPiece,
                 position: Vector2):
        self.paths = path_dict
        self.piece = piece
        self.position = position

    def to_dict(self):
        paths_dict = {}
        for path_key in self.paths:
            double_tup_key = f'{tuple_to_string(path_key[0])}-{tuple_to_string(path_key[1])}'
            paths_dict[double_tup_key] = self.paths[path_key].to_dict()

        return {
            "piece": self.piece.to_dict(),
            "position": tuple_to_string(self.position.get_tuple()),
            "paths": paths_dict
        }

    @staticmethod
    def from_dict(value: Dict):
        path_dict: Dict[Tuple[Tuple[int, int], Tuple[int, int]], PathFindingTile]
        piece: IPiece
        position: Vector2

        _piece = PieceDeserializer.from_dict(value.get("piece"))
        _position = Vector2.from_tuple(cast(Tuple[int, int], string_to_tuple(value["position"])))
        _paths: Dict[Tuple[Tuple[int, int], Tuple[int, int]], PathFindingTile] = {}

        paths_to_loop = value["paths"]
        for key in paths_to_loop:
            working_key = key.replace('(', '').replace(')', '')
            split_keys = working_key.split('-')
            proper_keys: Tuple[Tuple[int, int], Tuple[int, int]] = (
                cast(Tuple[int, int], string_to_tuple(split_keys[0])),
                cast(Tuple[int, int], string_to_tuple(split_keys[1]))
            )
            path_value = paths_to_loop[key]
            _paths[proper_keys] = PathFindingTile.from_dict(path_value)

        return PlayerPathDict(_paths, _piece, _position)
