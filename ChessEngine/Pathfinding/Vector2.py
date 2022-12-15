from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass
class Vector2:
    x: int
    y: int

    def get_tuple(self) -> Tuple[int, int]:
        return self.x, self.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other: Vector2 | int) -> Vector2:
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __mod__(self, other: Vector2) -> Vector2:
        return Vector2(self.x % other.x, self.y % other.y)

    @staticmethod
    def Zero() -> Vector2:
        return Vector2Cache.zero

    @staticmethod
    def Up() -> Vector2:
        return Vector2Cache.up

    @staticmethod
    def Down() -> Vector2:
        return Vector2Cache.down

    @staticmethod
    def Left() -> Vector2:
        return Vector2Cache.left

    @staticmethod
    def UpLeft() -> Vector2:
        return Vector2Cache.upLeft

    @staticmethod
    def DownLeft() -> Vector2:
        return Vector2Cache.downLeft

    @staticmethod
    def Right() -> Vector2:
        return Vector2Cache.right

    @staticmethod
    def UpRight() -> Vector2:
        return Vector2Cache.upRight

    @staticmethod
    def DownRight() -> Vector2:
        return Vector2Cache.downRight

    @staticmethod
    def from_tuple(tup: Tuple[int, int]) -> Vector2:
        return Vector2(tup[0], tup[1])


class Vector2Cache:
    zero = Vector2(0, 0)
    up = Vector2(0, 1)
    down = Vector2(0, -1)
    left = Vector2(-1, 0)
    upLeft = Vector2(-1, 1)
    downLeft = Vector2(-1, -1)
    right = Vector2(1, 0)
    upRight = Vector2(1, 1)
    downRight = Vector2(1, -1)
