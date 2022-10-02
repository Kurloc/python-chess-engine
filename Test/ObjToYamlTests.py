import unittest

from Game.Board import Board
from Game.PrintDebugger import PrintDebugger
from Game.Pieces.Pawn import Pawn
from Pathfinding.Pathfinder import PathFinder
from Pathfinding.Vector2 import Vector2


class ObjToYamlTests(unittest.TestCase):
    def test_obj_yaml_base(self):
        board: Board = Board()
        test_vector = board.map[(0, 1)]
        board.map[(0, 3)].piece = Pawn(board.teams[1])

        pathfinding_results = PathFinder.FindPaths(board, test_vector)

        move_result = board.move_piece(test_vector, Vector2(0, 3), pathfinding_results)
        obj_to_yaml = PrintDebugger.obj_yaml(move_result)


if __name__ == '__main__':
    unittest.main()
