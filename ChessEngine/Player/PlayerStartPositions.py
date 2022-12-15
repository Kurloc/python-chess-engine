from dataclasses import dataclass
from enum import Enum, IntEnum

import pydantic

from ChessEngine.Pydantic.ArbitraryConfig import Config


class PlayerStartPositions(IntEnum):
    TOP = 0,
    BOTTOM = 1
