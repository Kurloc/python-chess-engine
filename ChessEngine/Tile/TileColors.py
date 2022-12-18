from dataclasses import dataclass
from enum import Enum, IntEnum

import pydantic

from ChessEngine.Pydantic.ArbitraryConfig import Config


class TileColors(IntEnum):
    NONE = 0
    BLACK = 1
    WHITE = 2
