import unittest

from Game.Board import Board
from Game.Pathfinding.AiMoveTreeLeaf import AiMoveTreeHead, AiMoveTreeLeaf
from Game.Pathfinding.Vector2 import Vector2
from Game.Pieces.Bishop import Bishop
from Game.Pieces.King import King
from Game.Pieces.Knight import Knight
from Game.Pieces.Pawn import Pawn
from Game.Pieces.Queen import Queen
from Game.Pieces.Rook import Rook
from Game.Player.AI.AIEngineUser import AiEngineUser
from Game.Player.PlayerStartPositions import PlayerStartPositions
from Game.Player.Team import Team
from Game.PrintDebugger import PrintDebugger
from Game.Tile.TileColors import TileColors
from Test.BoardFixture import BoardFixture

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

    def test_find_paths_pawn_forward(self):
        board_layout_override = [
            # TOP                                                 # BOTTOM
            # OF BOARD                                            # OF BOARD
            [None,    None, None, None, None, None, Pawn(b), Rook(b)],
            [None,    None, None, None, None, None, Pawn(b), Knight(b)],
            [None,    None, None, None, None, None, Pawn(b), Bishop(b)],
            [Pawn(w), None, None, None, None, None, None,    Queen(b)],
            [None,    None, None, None, None, None, Pawn(b), King(b)],
            [None,    None, None, None, None, None, Pawn(b), Bishop(b)],
            [None,    None, None, None, None, None, Pawn(b), Knight(b)],
            [None,    None, None, None, None, None, Pawn(b), Rook(b)],

        ]
        board: Board = Board(
            board_layout_override,
            teams=[w, b]
        )

        ai = AiEngineUser(board, [w, b], 10)
        ai.output_player_turn_started(1)

        paths = board.get_all_paths_for_player(1)
        best_move = ai._find_best_move(paths)

        assert best_move[0].get_tuple() == (3, 0) and best_move[1].get_tuple() == (3, 1)

    def test_find_paths_full_board(self):
        board: BoardFixture = BoardFixture()
        ai = AiEngineUser(board.board, [w, b], 3)
        ai.output_player_turn_started(1)

        paths = board.board.get_all_paths_for_player(1)
        best_move = ai._find_best_move(paths)

        assert best_move[0].get_tuple() == (3, 0) and best_move[1].get_tuple() == (3, 1)

    def test_AiMoveTreeLeaf(self):
        head: AiMoveTreeHead = AiMoveTreeHead()

        head.leaves[(0, 0)] = AiMoveTreeLeaf(0, 0, Vector2(0, 0), Vector2(0, 0))
        zero_zero_leaf = head.leaves[(0, 0)]
        zero_zero_leaf.child_ai_move[(0, 1)] = AiMoveTreeLeaf(0, 0, Vector2(0, 0), Vector2(0, 1))
        zero_zero_leaf.child_ai_move[(1, 0)] = AiMoveTreeLeaf(0, 0, Vector2(0, 0), Vector2(1, 0))

        zero_zero_zero_one_leaf = head.leaves[(0, 0)].child_ai_move[(0, 1)]
        zero_zero_one_zero_leaf = head.leaves[(0, 0)].child_ai_move[(1, 0)]

        zero_zero_zero_one_leaf.child_ai_move[(0, 2)] = AiMoveTreeLeaf(0, 0, Vector2(0, 1), Vector2(0, 2))
        zero_zero_zero_one_leaf.child_ai_move[(1, 2)] = AiMoveTreeLeaf(0, 0, Vector2(0, 1), Vector2(1, 1))
        zero_zero_one_zero_leaf.child_ai_move[(1, 1)] = AiMoveTreeLeaf(0, 0, Vector2(1, 0), Vector2(1, 1))
        zero_zero_one_zero_leaf.child_ai_move[(2, 0)] = AiMoveTreeLeaf(0, 0, Vector2(1, 0), Vector2(2, 0))

        print(head)

    def test_print(self):
        board: BoardFixture = BoardFixture()
        ai = AiEngineUser(board.board, [w, b], 3)
        ai.output_player_turn_started(1)
        paths = board.board.get_all_paths_for_player(1)
        ai.build_move_tree(board.board, 1, paths)
