import unittest

from Game.Pathfinding.Vector2 import Vector2


class TestVector2(unittest.TestCase):
    def test_addition(self):
        test_vector2 = Vector2.Up() + Vector2.Up()
        self.assertEqual(test_vector2.y, 2)

    def test_multiplication(self):
        test_vector2 = Vector2.Up() * 5
        self.assertEqual(test_vector2.x, 0)
        self.assertEqual(test_vector2.y, 5)


if __name__ == '__main__':
    unittest.main()
