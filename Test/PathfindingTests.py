import unittest

from Game.Board import Board
from Game.Pieces.IPiece import WinConditions
from Game.PrintDebugger import PrintDebugger
from Game.Pieces.Pawn import Pawn
from Game.Tile.TileColors import TileColors
from Pathfinding.Vector2 import Vector2


class TestPathfinding(unittest.TestCase):
    """  X
      Y | |0|1|2|3|4|5|6|7|
        |0|R|K|B|K|Q|B|K|R|
        |1|P|P|P|P|P|P|P|P|
        |2|P| | | | | | | |
        |3| | | | | | | | |
        |4| | | | | | | | |
        |5| | | | | | | | |
        |6|P|P|P|P|P|P|P|P|
        |7|R|K|B|Q|K|B|K|R|
    """

    def test_findPaths_pawn_forward(self):
        board: Board = Board()
        test_vector = board.map[(0, 1)]
        board.map[(0, 3)].piece = Pawn(board.teams[1])

        pathfinding_results = board.FindPaths(test_vector)

        PrintDebugger.print_board(board)
        PrintDebugger.print_paths(pathfinding_results, test_vector)

        finalPosition = pathfinding_results[(0, 1)][(0, 3)]
        x0y2 = pathfinding_results[(0, 1)][(0, 2)]

        self.assertEqual(x0y2.isEnemy, False)
        self.assertEqual(x0y2.isBlocked, False)

        self.assertEqual(finalPosition.isEnemy, True)
        self.assertEqual(finalPosition.isBlocked, True)

    def test_findPaths_pawn_move_forward(self):
        board: Board = Board()
        test_tile_0 = board.map[(0, 1)]
        test_tile_1 = board.map[(1, 1)]
        test_tile_2 = board.map[(2, 1)]
        test_tile_3 = board.map[(3, 1)]
        original_piece = test_tile_0.piece

        board.map[(0, 3)].piece = Pawn(board.teams[1])

        pathfinding_results_0 = board.FindPaths(test_tile_0)
        pathfinding_results_1 = board.FindPaths(test_tile_1)
        pathfinding_results_2 = board.FindPaths(test_tile_2)
        pathfinding_results_3 = board.FindPaths(test_tile_3)

        print("Turn 1")
        PrintDebugger.print_board(board)

        move_results_0 = board.move_piece(test_tile_0, Vector2(0, 3), pathfinding_results_0)
        move_results_1 = board.move_piece(test_tile_1, Vector2(1, 3), pathfinding_results_1)
        move_results_2 = board.move_piece(test_tile_2, Vector2(2, 3), pathfinding_results_2)
        move_results_3 = board.move_piece(test_tile_3, Vector2(3, 3), pathfinding_results_3)

        self.assertTrue(move_results_0.success)
        self.assertEqual(len(move_results_0.pieces_involved), 2)
        self.assertEqual(board.map[(0, 3)].piece, original_piece)
        self.assertEqual(board.map[test_tile_0.position.get_tuple()].piece, None)

        print("Turn 2")
        PrintDebugger.print_board(board)

    def test_findPaths_checkmate(self):
        board: Board = Board()
        fst_move = board.map[(5, 6)]  # 1fwd
        snd_move = board.map[(4, 1)]  # 2fwd
        third_move = board.map[(6, 6)]  # 2fwd
        fourth_move = board.map[(3, 0)]  # all the way down right

        fst_path_results = board.FindPaths(fst_move)
        snd_path_results = board.FindPaths(snd_move)
        third_path_results = board.FindPaths(third_move)

        board.move_piece(fst_move, Vector2(5, 5), fst_path_results)
        board.move_piece(snd_move, Vector2(4, 2), snd_path_results)
        board.move_piece(third_move, Vector2(6, 4), third_path_results)

        fourth_path_results = board.FindPaths(fourth_move)
        fourth_move_results = board.move_piece(fourth_move, Vector2(7, 4), fourth_path_results)

        print("Turn 4")
        PrintDebugger.print_board(board)
        PrintDebugger.print_move_results(fourth_move_results)

        self.assertTrue(fourth_move_results.success)
        self.assertTrue(fourth_move_results.game_state.game_over)
        self.assertTrue(fourth_move_results.game_state.win_condition == WinConditions.CHECKMATE)
        self.assertTrue(fourth_move_results.game_state.winning_tile_pos.get_tuple() == (7, 4))
        self.assertTrue(fourth_move_results.game_state.winning_team.color == TileColors.WHITE)


if __name__ == '__main__':
    unittest.main()
