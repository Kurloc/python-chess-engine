import unittest

from parameterized import parameterized

from ChessEngine.Board.Board import Board
from ChessEngine.Board.WinConditions import WinConditions
from ChessEngine.Pieces.Bishop import Bishop
from ChessEngine.Pieces.King import King
from ChessEngine.Pieces.Knight import Knight
from ChessEngine.Pieces.Queen import Queen
from ChessEngine.Pieces.Rook import Rook
from ChessEngine.Debugging.PrintDebugger import PrintDebugger
from ChessEngine.Pieces.Pawn import Pawn
from ChessEngine.Tile.TileColors import TileColors
from ChessEngine.Pathfinding.Vector2 import Vector2
from Tests.BoardFixture import BoardFixture
from Tests.TestAiEngineUser import b, w

board_fixture = BoardFixture()
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
    board_fixture = BoardFixture()

    def test_find_paths_pawn_forward(self):
        board: Board = Board()
        test_vector = board.map[(0, 1)]
        starting_piece = test_vector.piece

        board.map[(1, 2)].piece = Pawn(board.teams[1])

        pathfinding_results = board.find_paths(test_vector)

        # print("Turn 1")
        # PrintDebugger.print_board(board.map, board.game_board_size)
        # PrintDebugger.print_paths(pathfinding_results, test_vector)

        x0y2 = pathfinding_results[(1, 1)][(1, 2)]
        self.assertEqual(x0y2.is_enemy, True)
        self.assertEqual(x0y2.is_blocked, True)

        move_result = board.move_piece(test_vector, Vector2(1, 2), pathfinding_results, 1)
        # PrintDebugger.print_move_results(move_result)

        # print("Turn 2")
        # PrintDebugger.print_board(board.map, board.game_board_size)

        self.assertTrue(move_result.success)
        self.assertTrue(len(move_result.pieces_involved) == 2)
        self.assertTrue(move_result)
        self.assertEqual(board.map[(1, 2)].piece, starting_piece)

    def test_find_paths_pawn_cant_kill_in_front(self):
        board: Board = Board()
        test_vector = board.map[(0, 1)]
        starting_piece = Pawn(board.teams[1])

        board.map[(0, 3)].piece = starting_piece

        pathfinding_results = board.find_paths(test_vector)

        print("Turn 1")
        PrintDebugger.print_board(board.map, board.game_board_size)
        # PrintDebugger.print_paths(pathfinding_results, test_vector)

        # x0y2 = pathfinding_results[(0, 1)][(0, 3)]
        # self.assertEqual(x0y2.is_enemy, True)
        # self.assertEqual(x0y2.is_blocked, True)

        move_result = board.move_piece(test_vector, Vector2(0, 3), pathfinding_results, 1)
        print(PrintDebugger.print_move_results(move_result))

        print("Turn 2")
        PrintDebugger.print_board(board.map, board.game_board_size)

        self.assertFalse(move_result.success)
        self.assertTrue(move_result)
        self.assertEqual(board.map[(0, 3)].piece, starting_piece)

    def test_find_paths_pawn_diagonal_attack(self):
        board: Board = Board()
        test_vector = board.map[(0, 1)]
        board.map[(0, 3)].piece = Pawn(board.teams[1])

        pathfinding_results = board.find_paths(test_vector)
        # PrintDebugger.print_paths(pathfinding_results, test_vector)

        finalPosition = pathfinding_results[(0, 1)][(0, 3)]
        x0y2 = pathfinding_results[(0, 1)][(0, 2)]

        self.assertEqual(x0y2.is_enemy, False)
        self.assertEqual(x0y2.is_blocked, False)

        self.assertEqual(finalPosition.is_enemy, True)
        self.assertEqual(finalPosition.is_blocked, True)

    def test_find_paths_pawn_move_forward(self):
        board: Board = Board()
        board.map[(0, 3)].piece = Pawn(board.teams[1])
        test_tile_0 = board.map[(0, 1)]
        dest_tile = board.map[(0, 3)]
        starting_piece = test_tile_0.piece
        original_piece = dest_tile.piece

        pathfinding_results_0 = board.find_paths(test_tile_0)

        # print("Turn 1")
        # PrintDebugger.print_board(board.map, board.game_board_size)

        move_results_0 = board.move_piece(test_tile_0, Vector2(0, 3), pathfinding_results_0, 1)

        self.assertFalse(move_results_0.success)
        self.assertEqual(len(move_results_0.pieces_involved), 1)
        self.assertEqual(board.map[(0, 3)].piece, original_piece)
        self.assertEqual(board.map[test_tile_0.position.get_tuple()].piece, starting_piece)

        # print("Turn 2")
        # PrintDebugger.print_board(board.map, board.game_board_size)

    def test_pawns_can_only_move_two_on_init(self):
        board: Board = Board()
        test_tile_0 = board.map[(0, 1)]
        test_tile_3 = board.map[(0, 3)]

        pathfinding_results_0 = board.find_paths(test_tile_0)
        move_results_0 = board.move_piece(test_tile_0, Vector2(0, 3), pathfinding_results_0, 1)

        pathfinding_results_1 = board.find_paths(test_tile_3)
        move_results_1 = board.move_piece(test_tile_3, Vector2(0, 5), pathfinding_results_1, 1)
        self.assertTrue(move_results_0.success)
        self.assertFalse(move_results_1.success)

    def test_pawns_can_move_along_edges_of_board(self):
        board: Board = Board(
            [
                # TOP                                                 # BOTTOM
                # OF BOARD                                            # OF BOARD
                [Pawn(w), None, None, None, None, None, Pawn(b), Rook(b)],
                [None, None, None, None, None, None, Pawn(b), Knight(b)],
                [None, None, None, None, None, None, Pawn(b), Bishop(b)],
                [None, None, None, None, None, None, None, Queen(b)],
                [None, None, None, None, None, None, Pawn(b), King(b)],
                [None, None, None, None, None, None, Pawn(b), Bishop(b)],
                [None, None, None, None, None, None, Pawn(b), Knight(b)],
                [Pawn(w), None, None, None, None, None, Pawn(b), Rook(b)],
            ],
            teams=[self.board_fixture.teams[0], self.board_fixture.teams[1]]
        )

        test_tile_0 = board.map[(7, 0)]
        test_tile_1 = board.map[(0, 0)]
        pathfinding_results_0 = board.find_paths(test_tile_0)
        pathfinding_results_1 = board.find_paths(test_tile_1)
        move_results_0 = board.move_piece(test_tile_0, Vector2(7, 2), pathfinding_results_0, 1)
        move_results_1 = board.move_piece(test_tile_1, Vector2(0, 1), pathfinding_results_1, 1)
        # PrintDebugger.print_board(board.map, board.game_board_size)
        self.assertTrue(move_results_0.success)
        self.assertTrue(move_results_1.success)

    def test_find_paths_checkmate(self):
        board: Board = Board()
        fst_move = board.map[(5, 6)]  # 1fwd
        snd_move = board.map[(4, 1)]  # 2fwd
        third_move = board.map[(6, 6)]  # 2fwd
        fourth_move = board.map[(3, 0)]  # all the way down right

        fst_path_results = board.find_paths(fst_move)
        snd_path_results = board.find_paths(snd_move)
        third_path_results = board.find_paths(third_move)

        fst_move_results = board.move_piece(fst_move, Vector2(5, 5), fst_path_results, 1)
        snd_move_results = board.move_piece(snd_move, Vector2(4, 2), snd_path_results, 1)
        third_move_results = board.move_piece(third_move, Vector2(6, 4), third_path_results, 1)

        # PrintDebugger.print_move_results(fst_move_results)
        # PrintDebugger.print_move_results(snd_move_results)
        # PrintDebugger.print_move_results(third_move_results)

        fourth_path_results = board.find_paths(fourth_move)
        fourth_move_results = board.move_piece(fourth_move, Vector2(7, 4), fourth_path_results, 1)

        # print("Turn 4")
        # PrintDebugger.print_board(board.map, board.game_board_size)
        # PrintDebugger.print_move_results(fourth_move_results)

        self.assertTrue(fourth_move_results.success)
        self.assertTrue(fourth_move_results.game_state.game_over)
        self.assertTrue(fourth_move_results.game_state.win_condition == WinConditions.CHECKMATE)
        self.assertTrue(fourth_move_results.game_state.winning_tile_pos.get_tuple() == (7, 4))
        self.assertTrue(fourth_move_results.game_state.winning_team.color == TileColors.WHITE)

    def test_find_paths_king_moves(self):
        board: Board = Board()
        fst_move = board.map[(4, 0)]  # 1fwd
        fst_path_results = board.find_paths(fst_move)
        fst_move_results = board.move_piece(fst_move, Vector2(4, 4), fst_path_results, 1)
        # PrintDebugger.print_move_results(fst_move_results)

        self.assertFalse(fst_move_results.success)
        self.assertFalse(fst_move_results.game_state.game_over)

    def test_find_paths_knight_moves(self):
        board: Board = Board()
        fst_move = board.map[(6, 0)]  # 1fwd
        board.map[(5, 2)].piece = Pawn(board.teams[1])
        fst_path_results = board.find_paths(fst_move)
        fst_move_results = board.move_piece(fst_move, Vector2(5, 2), fst_path_results, 1)
        # PrintDebugger.print_move_results(fst_move_results)

        self.assertTrue(fst_move_results.success)
        self.assertTrue(fst_move_results.board_event_type.PIECE_MOVED_TO_SPACE_AND_KILLED)
        self.assertFalse(fst_move_results.game_state.game_over)

    @parameterized.expand([
        (
                [
                    [Pawn(w), None, None, None, None, None, Pawn(b), Rook(b)],
                    [None, None, None, None, None, None, Pawn(b), Knight(b)],
                    [None, None, None, None, None, None, Pawn(b), Bishop(b)],
                    [None, None, None, None, None, None, None, Queen(b)],
                    [None, None, None, None, None, None, Pawn(b), King(b)],
                    [None, None, None, None, None, None, Pawn(b), Bishop(b)],
                    [None, None, None, Knight(b), None, None, Pawn(b), None],
                    [None, None, Pawn(w), None, None, None, Pawn(b), Rook(b)]
                ],
                (7, 2),
                (6, 3),
                True
        ),
        (
                [
                    [Pawn(w), None, Pawn(w), None, None, None, Pawn(b), Rook(b)],
                    [None, None, None, Knight(b), None, None, Pawn(b), Knight(b)],
                    [None, None, None, None, None, None, Pawn(b), Bishop(b)],
                    [None, None, None, None, None, None, None, Queen(b)],
                    [None, None, None, None, None, None, Pawn(b), King(b)],
                    [None, None, None, None, None, None, Pawn(b), Bishop(b)],
                    [None, None, None, None, None, None, Pawn(b), None],
                    [None, None, None, None, None, None, Pawn(b), Rook(b)]
                ],
                (0, 2),
                (1, 3),
                True,
                False
        ),
        (
                [
                    [Rook(w),   Pawn(w), None,      Knight(b), None,     Bishop(w), None,    Rook(b)],
                    [Knight(w), Pawn(w), None,      None,      None,     Pawn(b),   None,    None],
                    [Bishop(w), Pawn(w), None,      None,      Queen(b), None,      None,    Bishop(b)],
                    [None,      None,    None,      None,      None,     None,      Pawn(b), None],
                    [King(w),   None,    None,      None,      None,     None,      Pawn(b), King(b)],
                    [None,      None,    None,      None,      Pawn(w),  None,      Pawn(b), Bishop(b)],
                    [None,      Pawn(w), None,      None,      None,     None,      Pawn(b), Knight(b)],
                    [Rook(w),   Pawn(w), Knight(w), None,      Queen(w), None,      Pawn(b), Rook(b)]
                ],
                (2, 4),
                (2, 2),
                True,
                False
        )
    ])
    def test_piece_attacks(self, board_map, start_pos, end_pos, expected, checkmate=False):
        print('================================test_piece_attacks======================================')
        board: Board = Board(board_map, teams=[board_fixture.teams[0], board_fixture.teams[1]])
        PrintDebugger.print_board(board.map, board.game_board_size)

        test_tile_0 = board.map[start_pos]
        pathfinding_results_0 = board.find_paths(test_tile_0)
        move_results_0 = board.move_piece(test_tile_0, Vector2(end_pos[0], end_pos[1]), pathfinding_results_0, 1)

        PrintDebugger.print_board(board.map, board.game_board_size)
        assert move_results_0.success == expected
        if checkmate:
            assert move_results_0.game_state.game_over
            assert move_results_0.game_state.win_condition == WinConditions.CHECKMATE
        else:
            assert not move_results_0.game_state.game_over
            assert move_results_0.game_state.win_condition is None
        print('==================================================================================')


if __name__ == '__main__':
    unittest.main()
