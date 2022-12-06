import unittest
from typing import Tuple, List

from parameterized import parameterized

from ChessEngine.Board.Board import Board
from ChessEngine.Debugging.PrintDebugger import PrintDebugger
from ChessEngine.Pathfinding.MoveTree.MoveTreeHead import MoveTreeHead
from ChessEngine.Pathfinding.MoveTree.MoveTreeLeaf import MoveTreeLeaf
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.Pawn import Pawn
from ChessEngine.Player.AI.AIEngineUser import AiEngineUser
from ChessEngine.Player.PlayerStartPositions import PlayerStartPositions
from ChessEngine.Player.Team import Team
from ChessEngine.Tile.TileColors import TileColors
from Tests.BoardFixture import BoardFixture

(w, b) = (
    Team(TileColors.WHITE, PlayerStartPositions.TOP, 1),
    Team(TileColors.BLACK, PlayerStartPositions.BOTTOM, 2)
)


class TestPathfinding(unittest.TestCase):
    """  X
      Y | |0|1|2|3|4|5|6|7|
        |0|R|K|B|K|Q|B|K|R|
        |1|P|P|P| |P|P| |P|
        |2| | | | | | | | |
        |3| | | | | | | | |
        |4| | | | | | | | |
        |5| | | |p| | |p| |
        |6|P|P|P|P|P|P|P|P|
        |7|R|K|B|Q|K|B|K|R|


        |------->(3, 5)-(2, 6)
        |       |------>(2, 6)-(1, 7)
        |       |     |---->(6, 5)-(5, 6)
        |       |     |---->(6, 5)-(7, 6)
        |       |----->(2, 6)-(3, 7)
        |       |    |----->(6, 5)-(5, 6)
        |       |    |----->(6, 5)-(7, 6)
        |       |----->(6, 5)-(7, 6)
        |       |    |------>(2, 6)-(1, 7)
        |       |    |------>(2, 6)-(3, 7)
        |       |----->(6, 5)-(5, 6)
                     |------>(2, 6)-(1, 7)
                     |------>(2, 6)-(3, 7)

        (6, 5)
        |------->(4, 6)

        (6, 5)
        |------->(6, 5)-(5, 6)

        (6, 5)
        |------->(6, 5)-(7, 6)


    """
    #
    # def test_find_paths_pawn_forward(self):
    #     board_layout_override = [
    #         [None, None, None, None, Pawn(w), None, None, None],                      # 0
    #         [None, None, None, None, None,    None, None, None],                      # 1
    #         [None, None, None, None, None,    None, None, None],                      # 2
    #         [None, None, None, None, None,    None, None, None],                      # 3
    #         [None, None, None, None, None,    None, None, None],                      # 4
    #         [None, None, None, None, None,    None, None, None],                      # 5
    #         [None, None, None, None, None,    None, None, None],                      # 6
    #         [Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b)]  # 7
    #
    #     ]
    #     board: Board = Board(
    #         board_layout_override,
    #         teams=[w, b]
    #     )
    #
    #     ai = AiEngineUser(board, [w, b], 10)
    #     ai.output_player_turn_started(1)
    #
    #     paths = board.get_all_paths_for_player(1)
    #     best_move = ai._find_best_move(paths)
    #
    #     print(best_move)
    #     assert best_move[0].get_tuple() == (4, 0) and best_move[1].get_tuple() == (4, 1)
    #
    # def test_find_paths_full_board(self):
    #     board: BoardFixture = BoardFixture()
    #     ai = AiEngineUser(board.board, [w, b], 3)
    #     ai.output_player_turn_started(1)
    #
    #     paths = board.board.get_all_paths_for_player(1)
    #     best_move = ai._find_best_move(paths)
    #
    #     assert best_move is not None
    #
    # def test_AiMoveTreeLeaf(self):
    #     head: MoveTreeHead = MoveTreeHead()
    #
    #     head.leaves[(0, 0)] = MoveTreeLeaf(0, 0, Vector2(0, 0), Vector2(0, 0))
    #     zero_zero_leaf = head.leaves[(0, 0)]
    #     zero_zero_leaf.child_ai_move[(0, 1)] = MoveTreeLeaf(0, 0, Vector2(0, 0), Vector2(0, 1))
    #     zero_zero_leaf.child_ai_move[(1, 0)] = MoveTreeLeaf(0, 0, Vector2(0, 0), Vector2(1, 0))
    #
    #     zero_zero_zero_one_leaf = head.leaves[(0, 0)].child_ai_move[(0, 1)]
    #     zero_zero_one_zero_leaf = head.leaves[(0, 0)].child_ai_move[(1, 0)]
    #
    #     zero_zero_zero_one_leaf.child_ai_move[(0, 2)] = MoveTreeLeaf(0, 0, Vector2(0, 1), Vector2(0, 2))
    #     zero_zero_zero_one_leaf.child_ai_move[(1, 2)] = MoveTreeLeaf(0, 0, Vector2(0, 1), Vector2(1, 1))
    #     zero_zero_one_zero_leaf.child_ai_move[(1, 1)] = MoveTreeLeaf(0, 0, Vector2(1, 0), Vector2(1, 1))
    #     zero_zero_one_zero_leaf.child_ai_move[(2, 0)] = MoveTreeLeaf(0, 0, Vector2(1, 0), Vector2(2, 0))
    #
    #     print(head)

    @parameterized.expand([
        (
                """
                 ║0║1║2║3║4║5║6║7║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╬═
                0║r║n║b║q║k║b║n║r║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                1║p║p║p║p║ ║p║p║p║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                2║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                3║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                4║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                5║ ║ ║ ║ ║p║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                6║P║P║P║P║P║P║P║P║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                7║R║N║B║Q║K║B║N║R║
                """,
                [(4, 5)]
        ),
        (
                """
                 ║0║1║2║3║4║5║6║7║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╬═
                0║r║n║b║q║k║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                1║p║p║p║p║p║p║ ║p║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                2║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                3║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                4║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                5║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                6║P║P║P║P║P║P║P║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                7║R║N║B║Q║K║B║N║R║
                """,
                [(7, 1)]
        )
    ])
    def test_ai_best_move(self, board_map: str, expected_move: List[Tuple[int, int]]):
        print(f'================================test_ai_best_move======================================')
        init_board_map = PrintDebugger.get_init_map_from_printed_board(board_map, [w, b])
        bf = BoardFixture(init_board_map, [w, b])
        PrintDebugger.print_board(bf.board.map, bf.board.game_board_size)
        try:
            ai = AiEngineUser(bf.board, [w, b], 3)
            ai.output_player_turn_started(2)

            for move in expected_move:
                paths = bf.board.get_all_paths_for_player(2)
                best_move = ai._find_best_move(paths)
                bf.move_piece(best_move[0].get_tuple(), best_move[1].get_tuple())
                print('best move:', best_move)
                assert best_move is not None
                assert best_move[1] == Vector2(move[0], move[1])

        except Exception:
            raise
        print('==================================================================================')
