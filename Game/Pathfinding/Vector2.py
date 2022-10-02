from __future__ import annotations

class Vector2:
    x: int
    y: int

    def get_tuple(self) -> (int, int):
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
        return Vector2(0, 0)

    @staticmethod
    def Up() -> Vector2:
        return Vector2(0, 1)

    @staticmethod
    def Down() -> Vector2:
        return Vector2(0, -1)

    @staticmethod
    def Left() -> Vector2:
        return Vector2(-1, 0)

    @staticmethod
    def UpLeft() -> Vector2:
        return Vector2(-1, 1)

    @staticmethod
    def DownLeft() -> Vector2:
        return Vector2(-1, -1)

    @staticmethod
    def Right() -> Vector2:
        return Vector2(1, 0)

    @staticmethod
    def UpRight() -> Vector2:
        return Vector2(1, 1)

    @staticmethod
    def DownRight() -> Vector2:
        return Vector2(1, -1)


